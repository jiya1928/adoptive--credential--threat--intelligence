import hashlib
import requests


def check_password_breach(password):

    try:

        sha1_password = hashlib.sha1(
            password.encode()
        ).hexdigest().upper()

        prefix = sha1_password[:5]
        suffix = sha1_password[5:]

        url = (
            f"https://api.pwnedpasswords.com/range/{prefix}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:

            return {
                "status": "error",
                "message": "Could not contact breach database"
            }

        hashes = response.text.splitlines()

        for line in hashes:

            hash_suffix, count = line.split(":")

            if hash_suffix == suffix:

                count = int(count)

                if count > 1000000:
                    severity = "Critical"
                elif count > 100000:
                    severity = "High"
                elif count > 10000:
                    severity = "Medium"
                else:
                    severity = "Low"

                return {
                    "breached": True,
                    "breach_count": count,
                    "severity": severity
                }

        return {
            "breached": False,
            "breach_count": 0,
            "severity": "Safe"
        }

    except Exception as e:

        return {
            "