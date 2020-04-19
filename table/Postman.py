from queue import Queue
#import inspect
from datetime import datetime

class Postman:
    """
    Central class which manages communication between all threads. Like in real delivery
    business, messages can be send and requested. Send messages are stored in a queue associated
    with a specific topic. Threads can request messages for a specific topic.

    Messages are enriched with information about the sender and a timestamp automatically. Note
    that each message can only be retrieved once! So multi-recipients messages are not supported.
    """

    def __init__(self, topics):
        # Stores messages in a queue accessible via the topic name
        self.mailbox = dict()
        for key in topics:
            self.mailbox[key] = Queue(maxsize=3)

    def send(self, topic, msg):
        """
        Hand a messages over to the postman concerning a specified topic.
        """
        # Retrieve function caller from call stack
        # This line needs 20 sec for first execution!
        # sender = inspect.stack()[1][3]
        sender = 'Unknown'

        if topic in self.mailbox:
            package = dict(sender=sender, \
                           timestamp=datetime.now(), \
                           message=msg)
            self.mailbox[topic].put(package)
            return True
        else:
            print('[ERROR] Postman: Message from {0} could not be sent. Topic {1} not '
                  'available.'.format(sender, topic))
            return False

    def request(self, topic):
        """"
        Request a message concerning a specified topic. Note that each message is unique and can
        only retrieved once because it is deleted from the queue afterwards.

        Returns
        -------
        Dictionary containing sender, timestamp and message
        """
        if topic in self.mailbox:
            # Check if queue is empty
            if not self.mailbox[topic].empty():
                self.mailbox[topic].task_done()
                return self.mailbox[topic].get_nowait()
            else:
                return False
        else:
            # Retrieve function caller from call stack
            # This line needs 20 sec for first execution!
            # caller = inspect.stack()[1][3]
            caller = 'Unknown'
            print('[ERROR] Postman: Requested topic {0} not available for delivery to {1}'.format(
                topic, caller))
            return False




