from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple
from hash_utils import to_sha256
from crypto_utils import KeyPair, Signature


def op_message(sender_id: str, receiver_id: str, amount: int) -> bytes:
    return f"{sender_id}|{receiver_id}|{amount}".encode("utf-8")


@dataclass
class Account:
    account_id: str
    wallet: List[KeyPair] = field(default_factory=list)
    balance: int = 0

    @staticmethod
    def gen_account() -> "Account":
        kp = KeyPair.gen()
        account_id = to_sha256(kp.public_key_pem.decode("utf-8"))[:16]
        return Account(account_id=account_id, wallet=[kp], balance=0)

    def add_keypair(self) -> None:
        self.wallet.append(KeyPair.gen())

    def update_balance(self, delta: int) -> None:
        self.balance += int(delta)

    def create_payment_op(self, receiver: "Account", amount: int, key_index: int = 0) -> "Operation":
        amount = int(amount)
        kp = self.wallet[key_index]
        msg = op_message(self.account_id, receiver.account_id, amount)
        sig = Signature.sign(kp.private_key_pem, msg)
        return Operation(
            sender_id=self.account_id,
            receiver_id=receiver.account_id,
            amount=amount,
            sender_public_key_pem=kp.public_key_pem,
            signature=sig,
        )


@dataclass
class Operation:
    sender_id: str
    receiver_id: str
    amount: int
    sender_public_key_pem: bytes
    signature: bytes

    def verify_operation(self, coin_db: Dict[str, int]) -> bool:
        if self.amount <= 0:
            return False
        if self.sender_id not in coin_db:
            return False
        if coin_db[self.sender_id] < self.amount:
            return False
        msg = op_message(self.sender_id, self.receiver_id, self.amount)
        return Signature.verify(self.sender_public_key_pem, msg, self.signature)

    def op_fingerprint(self) -> Tuple[str, str, int, str]:
        return (
            self.sender_id,
            self.receiver_id,
            int(self.amount),
            to_sha256(self.signature.hex())[:16],
        )


@dataclass
class Transaction:
    transaction_id: str
    operations: List[Operation]
    nonce: int

    @staticmethod
    def create(operations: List[Operation], nonce: int) -> "Transaction":
        parts = [f"{op.sender_id}>{op.receiver_id}:{op.amount}:{to_sha256(op.signature.hex())[:8]}" for op in operations]
        base = "|".join(parts) + f"|{int(nonce)}"
        tx_id = to_sha256(base)
        return Transaction(transaction_id=tx_id, operations=operations, nonce=int(nonce))


@dataclass
class Block:
    block_id: str
    prev_hash: str
    transactions: List[Transaction]

    @staticmethod
    def create(transactions: List[Transaction], prev_hash: str) -> "Block":
        base = prev_hash + "|" + "|".join([tx.transaction_id for tx in transactions])
        block_id = to_sha256(base)
        return Block(block_id=block_id, prev_hash=prev_hash, transactions=transactions)


@dataclass
class Blockchain:
    coin_db: Dict[str, int] = field(default_factory=dict)
    block_history: List[Block] = field(default_factory=list)
    tx_db: Set[str] = field(default_factory=set)
    faucet_coins: int = 1000

    def init_blockchain(self) -> None:
        genesis = Block.create(transactions=[], prev_hash="0" * 64)
        self.block_history.append(genesis)

    def get_token_from_faucet(self, account: Account, amount: int = 100) -> None:
        amount = int(amount)
        if amount <= 0:
            return
        if self.faucet_coins <= 0:
            return
        if amount > self.faucet_coins:
            amount = self.faucet_coins

        self.faucet_coins -= amount
        self.coin_db[account.account_id] = self.coin_db.get(account.account_id, 0) + amount
        account.update_balance(amount)

    def _apply_transaction(self, tx: Transaction) -> None:
        for op in tx.operations:
            self.coin_db[op.sender_id] -= op.amount
            self.coin_db[op.receiver_id] = self.coin_db.get(op.receiver_id, 0) + op.amount

    def validate_block(self, block: Block) -> bool:
        last_block = self.block_history[-1]

        if block.prev_hash != last_block.block_id:
            return False

        for tx in block.transactions:
            if tx.transaction_id in self.tx_db:
                return False

        temp_db = dict(self.coin_db)

        for tx in block.transactions:
            used_ops = set()
            for op in tx.operations:
                fp = op.op_fingerprint()
                if fp in used_ops:
                    return False
                used_ops.add(fp)

                if op.receiver_id not in temp_db:
                    temp_db[op.receiver_id] = temp_db.get(op.receiver_id, 0)

                if not op.verify_operation(temp_db):
                    return False

                temp_db[op.sender_id] -= op.amount
                temp_db[op.receiver_id] += op.amount

        self.block_history.append(block)
        for tx in block.transactions:
            self.tx_db.add(tx.transaction_id)
            self._apply_transaction(tx)

        return True
