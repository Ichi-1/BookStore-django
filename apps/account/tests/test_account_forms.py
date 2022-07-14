import pytest
from apps.account.forms import (
    SignUpForm,
    UserAddressForm
)


@pytest.mark.parametrize(
    "full_name, phone, address_line, address_line2, town_city, postcode, validity",
    [
        ("mike", "02343343434", "add1", "add2", "town", "postcode", True),
        ("", "02343343434", "add1", "add2", "town", "postcode", False),
    ],
)
def test_customer_add(
        full_name, phone, address_line,
        address_line2, town_city, postcode, validity
):
    form = UserAddressForm(
        data={
            "full_name": full_name,
            "phone": phone,
            "address_line": address_line,
            "address_line2": address_line2,
            "town_city": town_city,
            "postcode": postcode,
        }
    )
    assert form.is_valid() is validity


def test_customer_create_address(client, customer):
    user = customer
    client.force_login(user)
    response = client.post(
        "/account/addresses/add",
        data={
            "full_name": "test",
            "phone": "test",
            "address_line": "test",
            "address_line2": "test",
            "town_city": "test",
            "postcode": "test",
        },
    )
    assert response.status_code == 302


@pytest.mark.parametrize(
    "name, email, password, password2, validity",
    [
        ("user1", "a@a.com", "12345a", "12345a", True),
        # ("user1", "a@a.com", "12345a", "", False),  # no second password
        # ("user1", "a@a.com", "", "12345a", False),  # no first password
        # ("user1", "a@a.com", "12345a", "12345b", False),  # password mismatch
        # ("user1", "", "12345a", "12345a", False),  # email
    ],
)
@pytest.mark.django_db
def test_create_account(name, email, password, password2, validity):
    form = SignUpForm(
        data={
            "name": name,
            "email": email,
            "password": password,
            "password2": password2,
        },
    )
    assert form.is_valid() is validity
