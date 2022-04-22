from project.models import Stock

def test_new_stock(new_stock):
    """
    GIVEN a Stock Model
    WHEN a new Stock object is created
    THEN check the symbol, number of shares, and purchase price fields are defined correctly
    """
    assert new_stock.stock_symbol == 'TSLA'
    assert new_stock.number_of_shares == 23
    assert new_stock.purchase_price == 22497

def test_new_user(new_user):
    """
    GIVEN a User Model
    WHEN a new User is created
    THEN check email and password is not stored as simple text
    """
    assert new_user.email == 'nipunsadvilkar@gmail.com'
    assert new_user.password_hashed != 'TestDriven10'