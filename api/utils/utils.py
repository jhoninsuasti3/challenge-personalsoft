from api.schemas.orders import WorkOrderModel, OrderAndCustomerModel
from api.schemas.customer import CustomerModel


def format_data_response(order_data, customer_data):
    order_model = WorkOrderModel(**order_data.__dict__)
    customer_model = CustomerModel(**customer_data.__dict__)
    order_and_customer = OrderAndCustomerModel(work_order=order_model, customer=customer_model)
    return order_and_customer
