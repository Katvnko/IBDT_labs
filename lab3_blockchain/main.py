from models import Account, Transaction, Block, Blockchain


def print_state(bc: Blockchain, a: Account, b: Account) -> None:
    ba = bc.coin_db.get(a.account_id, 0)
    bb = bc.coin_db.get(b.account_id, 0)
    print("Стан балансів:")
    print(f"  {a.account_id}: {ba}")
    print(f"  {b.account_id}: {bb}")
    print()


def main():
    bc = Blockchain()
    bc.init_blockchain()

    alice = Account.gen_account()
    bob = Account.gen_account()

    bc.get_token_from_faucet(alice, 200)
    bc.get_token_from_faucet(bob, 50)

    print("Після faucet:")
    print_state(bc, alice, bob)

    op1 = alice.create_payment_op(bob, 30, 0)
    tx1 = Transaction.create([op1], nonce=1)

    op2 = bob.create_payment_op(alice, 10, 0)
    tx2 = Transaction.create([op2], nonce=2)

    last_hash = bc.block_history[-1].block_id
    block1 = Block.create([tx1, tx2], prev_hash=last_hash)

    ok = bc.validate_block(block1)

    print("Додавання блоку:", "успішно" if ok else "помилка")
    print("ID блоку:", block1.block_id)
    print("PrevHash:", block1.prev_hash)
    print()

    print("Після додавання блоку:")
    print_state(bc, alice, bob)

    bad_block = Block.create([tx1], prev_hash=bc.block_history[-1].block_id)
    ok2 = bc.validate_block(bad_block)
    print("Повтор транзакції в новому блоці:", "успішно" if ok2 else "відхилено (дубль)")

    # нова транзакція
    op3 = alice.create_payment_op(bob, 20, 0)
    tx3 = Transaction.create([op3], nonce=3)

    last_hash = bc.block_history[-1].block_id
    block2 = Block.create([tx3], prev_hash=last_hash)

    ok3 = bc.validate_block(block2)
    print("Другий переказ:", "успішно" if ok3 else "помилка")

    print_state(bc, alice, bob)

if __name__ == "__main__":
    main()
