#         # TODO: implement asynchronous notification with retry / backoff

import httpx
import asyncio
from src.core.logging import logger


class NotifyService:
    def __init__(self):
        self.notify_url = "http://mock-external-api:9000/notify"
        self.max_retries = 3
        self.base_delay = 1  # seconds

    async def send_notification(
        self,
        ticket_id: str,
        tenant_id: str,
        urgency: str,
        reason: str
    ):
        """
        Send notification asynchronously with manual retry + backoff.
        Must NEVER raise to caller.
        """

        payload = {
            "ticket_id": ticket_id,
            "tenant_id": tenant_id,
            "urgency": urgency,
            "reason": reason,
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    response = await client.post(self.notify_url, json=payload)

                if response.status_code < 300:
                    logger.info(
                        f"Notification sent for ticket={ticket_id} (attempt {attempt})"
                    )
                    return

                logger.warning(
                    f"Notify failed (status={response.status_code}) "
                    f"ticket={ticket_id}, attempt={attempt}"
                )

            except Exception as e:
                logger.warning(
                    f"Notify exception ticket={ticket_id}, attempt={attempt}: {e}"
                )

            # Exponential backoff
            await asyncio.sleep(self.base_delay * attempt)

        logger.error(
            f"Notification permanently failed for ticket={ticket_id}"
        )
