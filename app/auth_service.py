"""
Authentication-related services.
Responsible only for verifying customer credentials
and returning associated plant data.
"""

from sheets import find_plants_by_customer


def authenticate_customer(customer_id, password):
    """
    Authenticates a customer using customer_id and password.

    A customer can have multiple plants.
    Password is assumed to be same for all plants.

    Returns:
        (plants, None) on success
        (None, error_message) on failure
    """

    # Fetch all plants belonging to this customer
    plants = find_plants_by_customer(customer_id)

    if not plants:
        return None, "Invalid customer ID"

    # Password check (same password across customer's plants)
    if plants[0].get("password") != password:
        return None, "Invalid password"

    # Remove sensitive data before returning
    for plant in plants:
        plant.pop("password", None)

    return plants, None
