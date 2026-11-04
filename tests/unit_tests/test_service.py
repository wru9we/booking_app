import pytest
from users.service import UserService

@pytest.mark.parametrize("user_id,email,is_present", [
    (1, "test@test.com", True),
    (2, "wru9we@example.com", True),
    (3, ".....", False)
])
async def test_find_by_id(user_id, email, is_present):
    user = await UserService.find_by_id(user_id)

    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user