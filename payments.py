from tronpy import Tron as wallet_tron
from tronapi import Tron


def create_user_wallet():
    client = wallet_tron()
    usdt_wallet = client.generate_address()
    return usdt_wallet


def make_payment(wallet_transfer_to, wallet_transfer_from, amount):
    full_node = 'https://api.trongrid.io'
    solidity_node = 'https://api.trongrid.io'
    event_server = 'https://api.trongrid.io'

    pkey = wallet_transfer_from.private_key

    payments = [
        [amount, wallet_transfer_to.address],
    ]

    tron = Tron(full_node=full_node,
                solidity_node=solidity_node,
                event_server=event_server)

    tron.private_key = pkey
    tron.default_address = tron.address.from_private_key(pkey).base58

    for payment_amount, payment_address in payments:
        trx_kwargs = dict()
        trx_kwargs["private_key"] = pkey
        trx_kwargs["default_address"] = tron.address.from_private_key(pkey).base58

        tron = Tron(**trx_kwargs)

        kwargs = dict()
        kwargs["contract_address"] = tron.address.to_hex("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")  # USDT contract address
        kwargs[
            "function_selector"] = "transfer(address,uint256)"
        kwargs["fee_limit"] = 5000000
        kwargs["call_value"] = 0

        payment_amount = int(float(payment_amount))
        kwargs["parameters"] = [
            {
                'type': 'address',
                'value': tron.address.to_hex(payment_address)
            },
            {
                'type': 'uint256',
                'value': payment_amount * 1000000  # 1000000 = 1 USDT
            }
        ]

        raw_tx = tron.transaction_builder.trigger_smart_contract(**kwargs)
        signed = tron.trx.sign(raw_tx["transaction"])
        result = tron.trx.broadcast(signed)

        return result
