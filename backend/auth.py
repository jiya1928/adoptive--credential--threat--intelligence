from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):

    return pwd_context.hash(
        password
    )

def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def validate_password_strength(
    password: str
):

    issues = []

    if len(password) < 8:
        issues.append(
            "Password must be at least 8 characters"
        )

    if not any(
        char.isupper()
        for char in password
    ):
        issues.append(
            "Add an uppercase letter"
        )

    if not any(
        char.islower()
        for char in password
    ):
        issues.append(
            "Add a lowercase letter"
        )

    if not any(
        char.isdigit()
        for char in password
    ):
        issues.append(
            "Add a number"
        )

    if not any(
        char in "!@#$%^&*()_-+=<>?"
        for char in password
    ):
        issues.append(
            "Add a special character"
        )

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }