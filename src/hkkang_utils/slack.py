import contextlib
import logging
import os
from typing import *

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import hkkang_utils.misc as misc_utils
import hkkang_utils.socket as socket_utils

# Load environment variables
misc_utils.load_dotenv(stack_depth=2)

DEFAULT_ACCESS_TOKEN = os.environ.get("SLACK_ACCESS_TOKEN")

logger = logging.getLogger("SlackMessenger")


class SlackMessenger:
    """A Slack messaging wrapper for sending messages with an optional short preview."""

    def __init__(
        self,
        channel: str,
        token: str = DEFAULT_ACCESS_TOKEN,
        append_src_info: bool = True,
    ):
        self.channel = channel
        self.token = token
        self.append_src_info = append_src_info
        self.__post_init__()

    def __post_init__(self):
        if not self.token:
            raise ValueError(
                """Please set token or SLACK_ACCESS_TOKEN environment variable.
                   Follow the tutorial to set up bot OAuthToken and permissions: 
                   https://github.com/slackapi/python-slack-sdk/tree/main/tutorial"""
            )

    def send(self, text: str, comments: Optional[List[str]] = None) -> None:
        """Send a Slack message with an optional comment."""
        send_message(
            token=self.token,
            channel=self.channel,
            text=text,
            comments=comments,
            append_src_info=self.append_src_info,
        )


def send_message(
    channel: str,
    text: str,
    token: str = DEFAULT_ACCESS_TOKEN,
    comments: Optional[List[str]] = None,
    append_src_info: bool = True,
) -> None:
    """Send a Slack message with an optional comment."""

    if not token:
        raise ValueError("Please set SLACK_ACCESS_TOKEN environment variable.")

    client = WebClient(token=token)

    if append_src_info:
        ip = socket_utils.get_local_ip()
        host_name = socket_utils.get_host_name()
        text_with_prefix = f"Message from {host_name} ({ip}):\n{text}"
    else:
        text_with_prefix = text

    # Send the message
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=text_with_prefix,
        )
    except SlackApiError as e:
        logger.error(f"Error sending text message: {e.response['error']}")

    # Send the comment
    if comments:
        for comment in comments:
            try:
                response = client.chat_postMessage(
                    channel=channel,
                    thread_ts=response["ts"],
                    text=comment,
                )
            except SlackApiError as e:
                logger.error(f"Error sending comment: {e.response['error']}")


@contextlib.contextmanager
def notification(
    channel: str,
    success_msg: str = None,
    error_msg: str = None,
    token: str = DEFAULT_ACCESS_TOKEN,
    comments: Optional[List[str]] = None,
    disable: bool = False,
    disable_callback: Callable = None,
) -> None:
    """Send a message when the task within the code block is finished, with an optional short preview.

    Example:
        import hkkang_utils.slack as slack_utils

        with slack_utils.notification(
            channel="test-channel",
            success_msg="Process done!",
            error_msg="Error raised during the process",
            comments=["This is a comment", "This is another comment"],
        ):
            # Perform your task here
            ...

    :param channel: Name of the channel to send the message
    :type channel: str
    :param success_msg: Message to send when the given code block completes, defaults to None
    :type success_msg: str, optional
    :param error_msg: Message to send when an error occurs, defaults to None
    :type error_msg: str, optional
    :param token: Slack access token, defaults to DEFAULT_ACCESS_TOKEN
    :type token: str, optional
    :param disable: Whether to disable Slack notifications, defaults to False
    :type disable: bool, optional
    :param comments: Comments to send, defaults to None
    :type comments: List[str], optional
    :rtype: None
    """
    if misc_utils.is_debugger_active():
        disable = True
        disable_callback = None

    if disable:
        yield None
        return None

    slack_messenger = SlackMessenger(channel=channel, token=token)
    try:
        yield slack_messenger
        # Check if the disable_callback is not None and if it returns True
        if disable_callback is not None and disable_callback():
            return None
        # Send the success message
        if success_msg is not None:
            slack_messenger.send(success_msg, comments=comments)
    except Exception as e:
        # Send the error message
        if error_msg is None:
            message_to_send = f"Error occurred at {e.__class__.__name__}: {e}"
        else:
            message_to_send = f"{error_msg} ({e.__class__.__name__}: {e})"
        # Check if the disable_callback is not None and if it returns True
        if disable_callback is not None and disable_callback():
            return None
        slack_messenger.send(message_to_send, comments=comments)
        raise e


@contextlib.contextmanager
def slack_notification(*args, **kwargs):
    raise NotImplementedError("Please use notification instead of slack_notification")
