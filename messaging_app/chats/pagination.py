from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages, setting a default page size of 20.
    """
    page_size = 20 # Number of messages per page
    page_size_query_param = 'page_size' # Allows client to specify page size (e.g., ?page_size=10)
    max_page_size = 100 # Maximum page size allowed if client requests more