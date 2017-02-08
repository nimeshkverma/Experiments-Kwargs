from activity.models import CustomerState


def get_homepage(customer_id):
    customer_present_state = CustomerState.get_customer_present_state(
        customer_id)
    return {
        "customer_id": customer_id,
        "customer_state": customer_present_state
    }
