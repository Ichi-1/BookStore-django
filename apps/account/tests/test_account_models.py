import pytest

def test_customer_str(customer):
    assert customer.__str__() == 'user1'


def test_admin_str(super_user):
    assert super_user.__str__() == 'admin'


def test_customer_email_no_input(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email='')

    assert str(e.value) == 'Customer Account: You must provide a email'


def test_customer_email_invalid(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email='a.com')
    
    assert str(e.value) == 'You must provide a valid email'



def test_admin_email_no_input(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email='', is_superuser=True, is_staff=True)

    assert str(e.value) == 'Superuser Account: You must provide a email'


def test_admin_email_invalid(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email='a.com', is_superuser=True, is_staff=True)

    assert str(e.value) == 'You must provide a valid email'



def test_admin_not_staff(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email='admin@admin.com', is_superuser=True, is_staff=False)

    assert str(e.value) == 'Superuser must be assigned to is_staff=True'


def test_admin_not_superuser(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email='admin@admin.com', is_superuser=False, is_staff=True)

    assert str(e.value) == 'Superuser must be assigned to is_superuser=True'


def test_address_str(address):
    full_name = address.full_name
    assert address.__str__() == f'{full_name} Address' 