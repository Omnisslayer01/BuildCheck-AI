def checkout(cart_total, user_wallet):
    # TODO: Add security later
    # BUG: Subtracts the wallet from the cart instead of cart from wallet!
    remaining_balance = cart_total - user_wallet
    return remaining_balance