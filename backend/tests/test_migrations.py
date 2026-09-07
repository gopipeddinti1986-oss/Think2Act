import os
import tempfile
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest

@pytest.mark.asyncio
async def test_alembic_migrations_from_clean_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_db_path = tmp.name

    try:
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        alembic_cfg = Config(os.path.join(backend_dir, "alembic.ini"))
        alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite+aiosqlite:///{tmp_db_path.replace(os.sep, '/')}")
        alembic_cfg.set_main_option("script_location", os.path.join(backend_dir, "migrations").replace(os.sep, '/'))

        import asyncio
        await asyncio.to_thread(command.upgrade, alembic_cfg, "head")

        sync_engine = create_engine(f"sqlite:///{tmp_db_path}")
        inspector = inspect(sync_engine)
        tables = inspector.get_table_names()

        # Verify all ORM models exist in the migrated database
        from app.models.base import Base
        for table_name in Base.metadata.tables.keys():
            assert table_name in tables, f"Expected model table '{table_name}' missing from migrated database."

        # Also verify alembic_version tracking table exists
        assert "alembic_version" in tables

        profile_cols = [c["name"] for c in inspector.get_columns("user_profiles")]
        assert "experience_level" in profile_cols
        assert "work_start_time" in profile_cols
        assert "notification_preferences" in profile_cols

        task_cols = [c["name"] for c in inspector.get_columns("tasks")]
        assert "source" in task_cols
        assert "dependencies" in task_cols

        sync_engine.dispose()

        async_db_url = f"sqlite+aiosqlite:///{tmp_db_path.replace(os.sep, '/')}"
        async_engine = create_async_engine(async_db_url, echo=False)
        session_factory = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

        async with session_factory() as session:
            auth_service = AuthService(session)
            reg_req = RegisterRequest(
                name="Migration Tester",
                email="migration@test.com",
                password="SecurePassword123!"
            )
            reg_res = await auth_service.register(reg_req)
            assert reg_res.user.email == "migration@test.com"
            assert reg_res.token.access_token is not None

            # Verify profile was created in DB
            db_user = await auth_service.user_repo.get_by_id(reg_res.user.id)
            assert db_user is not None
            assert db_user.profile is not None
            assert db_user.profile.user_mode == "student"

            login_req = LoginRequest(
                email="migration@test.com",
                password="SecurePassword123!"
            )
            login_res = await auth_service.login(login_req)
            assert login_res.user.email == "migration@test.com"

        await async_engine.dispose()

    finally:
        if os.path.exists(tmp_db_path):
            try:
                os.remove(tmp_db_path)
            except OSError:
                pass
