# sgt_sync/models/sgt.py
from dataclasses import dataclass

@dataclass
class SecurityGroupTag:
    """
    Represents a Security Group Tag in a normalized format.
    This model is used internally for diffing and synchronization.
    """
    key: str        # Unique identifier (e.g., ISE ID, SA UUID)
    label: str      # Display name of the SGT
    tag_id: int     # Numeric SGT value
    status: str     # "active" or "inactive"

    def to_sa_format(self) -> dict:
        """Converts the SGT to the format expected by Secure Access API."""
        return {
            "key": self.key,
            "label": self.label,
            "status": self.status,
            "tagId": self.tag_id,
        }

    @staticmethod
    def from_ise_data(ise_sgt_data: dict) -> "SecurityGroupTag":
        """
        Transforms raw ISE SGT data into the normalized SecurityGroupTag model.
        ISE 'id' is used as 'key' for comparison and identification.
        """
        if not all(k in ise_sgt_data for k in ["id", "name", "value"]):
            raise ValueError(f"Malformed ISE SGT data: {ise_sgt_data}")
        return SecurityGroupTag(
            key=ise_sgt_data["id"],
            label=ise_sgt_data["name"],
            tag_id=ise_sgt_data["value"],
            status="active",
        )

    @staticmethod
    def from_sa_data(sa_sgt_data: dict) -> "SecurityGroupTag":
        """
        Transforms raw Secure Access SGT data into the normalized SecurityGroupTag model.
        """
        if not all(k in sa_sgt_data for k in ["key", "label", "tagId", "status"]):
            raise ValueError(f"Malformed Secure Access SGT data: {sa_sgt_data}")
        return SecurityGroupTag(
            key=sa_sgt_data["key"],
            label=sa_sgt_data["label"],
            tag_id=sa_sgt_data["tagId"],
            status=sa_sgt_data["status"],
        )