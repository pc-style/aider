"""
Unit tests for Pentest AI core components
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

from pentest_ai.core import (
    MultiAgentOrchestrator,
    MCPClient,
    ContainerManager,
    GraphDatabase,
    SafetyGates,
    AuditLogger,
    AgentType,
    WorkflowStatus,
    LLMProvider,
    ContainerStatus,
    NodeType,
    SafetyLevel,
    LogLevel,
    EventType,
    Target,
    Session,
    Vulnerability,
    Credential
)


class TestMultiAgentOrchestrator:
    """Test MultiAgentOrchestrator"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance"""
        mcp_client = Mock(spec=MCPClient)
        graph_db = Mock(spec=GraphDatabase)
        safety_gates = Mock(spec=SafetyGates)
        audit_logger = Mock(spec=AuditLogger)
        
        return MultiAgentOrchestrator(
            mcp_client=mcp_client,
            graph_db=graph_db,
            safety_gates=safety_gates,
            audit_logger=audit_logger
        )
    
    def test_init(self, orchestrator):
        """Test orchestrator initialization"""
        assert orchestrator.mcp_client is not None
        assert orchestrator.graph_db is not None
        assert orchestrator.safety_gates is not None
        assert orchestrator.audit_logger is not None
        assert len(orchestrator.agents) == 0
        assert len(orchestrator.workflows) == 0
    
    @pytest.mark.asyncio
    async def test_register_agent(self, orchestrator):
        """Test agent registration"""
        agent_config = {
            "name": "test_agent",
            "type": AgentType.RECONNAISSANCE,
            "capabilities": ["port_scan", "service_detection"]
        }
        
        success = await orchestrator.register_agent(agent_config)
        assert success is True
        assert "test_agent" in orchestrator.agents
    
    @pytest.mark.asyncio
    async def test_create_workflow(self, orchestrator):
        """Test workflow creation"""
        workflow_id = await orchestrator.create_workflow(
            target="example.com",
            scope=["web", "network"],
            workflow_type="comprehensive"
        )
        
        assert workflow_id is not None
        assert workflow_id in orchestrator.workflows
    
    @pytest.mark.asyncio
    async def test_execute_workflow(self, orchestrator):
        """Test workflow execution"""
        # Create workflow first
        workflow_id = await orchestrator.create_workflow(
            target="example.com",
            scope=["web"],
            workflow_type="basic"
        )
        
        # Mock agent execution
        orchestrator.agents = {
            "recon_agent": Mock(spec=dict),
            "scan_agent": Mock(spec=dict)
        }
        
        result = await orchestrator.execute_workflow(workflow_id)
        assert result is not None
        assert hasattr(result, 'status')


class TestMCPClient:
    """Test MCPClient"""
    
    @pytest.fixture
    def mcp_client(self):
        """Create MCP client instance"""
        return MCPClient()
    
    def test_init(self, mcp_client):
        """Test MCP client initialization"""
        assert mcp_client.providers is not None
        assert len(mcp_client.providers) > 0
    
    @pytest.mark.asyncio
    async def test_send_message(self, mcp_client):
        """Test sending message"""
        with patch('pentest_ai.core.mcp_client.openai.ChatCompletion.create') as mock_openai:
            mock_openai.return_value = Mock(
                choices=[Mock(message=Mock(content="Test response"))]
            )
            
            response = await mcp_client.send_message(
                message="Hello",
                provider=LLMProvider.OPENAI
            )
            
            assert response is not None
            assert "Test response" in response
    
    @pytest.mark.asyncio
    async def test_get_available_providers(self, mcp_client):
        """Test getting available providers"""
        providers = await mcp_client.get_available_providers()
        assert isinstance(providers, list)
        assert len(providers) > 0


class TestContainerManager:
    """Test ContainerManager"""
    
    @pytest.fixture
    def container_manager(self):
        """Create container manager instance"""
        return ContainerManager()
    
    def test_init(self, container_manager):
        """Test container manager initialization"""
        assert container_manager.docker_client is not None
        assert len(container_manager.images) > 0
    
    @pytest.mark.asyncio
    async def test_create_container(self, container_manager):
        """Test container creation"""
        with patch('docker.from_env') as mock_docker:
            mock_container = Mock()
            mock_docker.return_value.containers.run.return_value = mock_container
            
            result = await container_manager.create_container(
                name="test_container",
                image="nmap:latest",
                command="nmap -sS example.com"
            )
            
            assert result is not None
            assert result.status == ContainerStatus.CREATED
    
    @pytest.mark.asyncio
    async def test_run_nmap_scan(self, container_manager):
        """Test nmap scan execution"""
        with patch.object(container_manager, 'create_container') as mock_create:
            mock_create.return_value = Mock(
                status=ContainerStatus.COMPLETED,
                exit_code=0,
                stdout="Port 80/tcp open",
                error=""
            )
            
            result = await container_manager.run_nmap_scan(
                target="example.com",
                scan_type="basic"
            )
            
            assert result is not None
            assert result.status == ContainerStatus.COMPLETED
            assert result.exit_code == 0


class TestGraphDatabase:
    """Test GraphDatabase"""
    
    @pytest.fixture
    def graph_db(self):
        """Create graph database instance"""
        return GraphDatabase()
    
    def test_init(self, graph_db):
        """Test graph database initialization"""
        assert graph_db.driver is not None
    
    @pytest.mark.asyncio
    async def test_create_target(self, graph_db):
        """Test target creation"""
        target = Target(
            id="test_target_1",
            name="example.com",
            type="domain",
            scope=["web", "network"],
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            metadata={}
        )
        
        with patch.object(graph_db, 'driver') as mock_driver:
            mock_session = Mock()
            mock_driver.session.return_value.__aenter__.return_value = mock_session
            
            success = await graph_db.create_target(target)
            assert success is True
    
    @pytest.mark.asyncio
    async def test_search_targets(self, graph_db):
        """Test target search"""
        with patch.object(graph_db, 'driver') as mock_driver:
            mock_session = Mock()
            mock_result = Mock()
            mock_result.data.return_value = [
                {"target": {"name": "example.com", "type": "domain"}}
            ]
            mock_session.run.return_value = mock_result
            mock_driver.session.return_value.__aenter__.return_value = mock_session
            
            targets = await graph_db.search_targets("example.com")
            assert isinstance(targets, list)
            assert len(targets) > 0


class TestSafetyGates:
    """Test SafetyGates"""
    
    @pytest.fixture
    def safety_gates(self):
        """Create safety gates instance"""
        return SafetyGates()
    
    def test_init(self, safety_gates):
        """Test safety gates initialization"""
        assert len(safety_gates.safety_rules) > 0
        assert len(safety_gates.blocked_targets) >= 0
    
    @pytest.mark.asyncio
    async def test_verify_consent(self, safety_gates):
        """Test consent verification"""
        consent_record = ConsentRecord(
            user_id="test_user",
            target="example.com",
            scope=["web"],
            timestamp=datetime.utcnow(),
            ip_address="127.0.0.1"
        )
        
        result = await safety_gates.verify_consent(consent_record)
        assert isinstance(result, bool)
    
    @pytest.mark.asyncio
    async def test_validate_target(self, safety_gates):
        """Test target validation"""
        result = await safety_gates.validate_target("example.com")
        assert isinstance(result, bool)
    
    @pytest.mark.asyncio
    async def test_comprehensive_safety_check(self, safety_gates):
        """Test comprehensive safety check"""
        checks = await safety_gates.comprehensive_safety_check(
            target="example.com",
            scope=["web"],
            tools=["nmap", "nikto"],
            user_id="test_user",
            operation_type="scan"
        )
        
        assert isinstance(checks, list)
        assert len(checks) > 0
        assert all(hasattr(check, 'passed') for check in checks)


class TestAuditLogger:
    """Test AuditLogger"""
    
    @pytest.fixture
    def audit_logger(self):
        """Create audit logger instance"""
        return AuditLogger()
    
    def test_init(self, audit_logger):
        """Test audit logger initialization"""
        assert audit_logger.db_path is not None
        assert audit_logger.log_dir is not None
    
    @pytest.mark.asyncio
    async def test_log_event(self, audit_logger):
        """Test event logging"""
        event = AuditEvent(
            id="test_event_1",
            timestamp=datetime.utcnow(),
            event_type=EventType.TARGET_CREATE,
            level=LogLevel.INFO,
            user_id="test_user",
            message="Test event",
            details={},
            target_id=None,
            workflow_id=None,
            session_id=None
        )
        
        success = await audit_logger.log_event(
            event_type=EventType.TARGET_CREATE,
            level=LogLevel.INFO,
            user_id="test_user",
            message="Test event"
        )
        
        assert success is True
    
    @pytest.mark.asyncio
    async def test_get_events(self, audit_logger):
        """Test event retrieval"""
        events = await audit_logger.get_events(
            start_time=datetime.utcnow() - timedelta(hours=1),
            end_time=datetime.utcnow(),
            limit=10
        )
        
        assert isinstance(events, list)
    
    @pytest.mark.asyncio
    async def test_get_statistics(self, audit_logger):
        """Test statistics retrieval"""
        stats = await audit_logger.get_statistics(
            start_time=datetime.utcnow() - timedelta(days=1),
            end_time=datetime.utcnow()
        )
        
        assert isinstance(stats, dict)
        assert "total_events" in stats


class TestDataModels:
    """Test data models"""
    
    def test_target_model(self):
        """Test Target model"""
        target = Target(
            id="test_target_1",
            name="example.com",
            type="domain",
            scope=["web", "network"],
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            metadata={"description": "Test target"}
        )
        
        assert target.id == "test_target_1"
        assert target.name == "example.com"
        assert "web" in target.scope
    
    def test_vulnerability_model(self):
        """Test Vulnerability model"""
        vuln = Vulnerability(
            id="test_vuln_1",
            title="SQL Injection",
            description="SQL injection vulnerability found",
            severity="high",
            cvss_score=8.5,
            cve_id="CVE-2023-1234",
            proof_of_concept="SELECT * FROM users",
            recommendation="Use parameterized queries",
            target_id="test_target_1",
            discovered_at=datetime.utcnow(),
            metadata={}
        )
        
        assert vuln.id == "test_vuln_1"
        assert vuln.severity == "high"
        assert vuln.cvss_score == 8.5
    
    def test_credential_model(self):
        """Test Credential model"""
        cred = Credential(
            id="test_cred_1",
            type="password",
            username="admin",
            password="password123",
            hash_type=None,
            hash_value=None,
            source="brute_force",
            target_id="test_target_1",
            discovered_at=datetime.utcnow(),
            metadata={}
        )
        
        assert cred.id == "test_cred_1"
        assert cred.username == "admin"
        assert cred.type == "password"


class TestEnums:
    """Test enum classes"""
    
    def test_agent_type_enum(self):
        """Test AgentType enum"""
        assert AgentType.RECONNAISSANCE == "reconnaissance"
        assert AgentType.VULNERABILITY_SCANNER == "vulnerability_scanner"
        assert AgentType.EXPLOITATION == "exploitation"
        assert AgentType.POST_EXPLOITATION == "post_exploitation"
        assert AgentType.REPORTING == "reporting"
    
    def test_workflow_status_enum(self):
        """Test WorkflowStatus enum"""
        assert WorkflowStatus.PENDING == "pending"
        assert WorkflowStatus.RUNNING == "running"
        assert WorkflowStatus.COMPLETED == "completed"
        assert WorkflowStatus.FAILED == "failed"
        assert WorkflowStatus.CANCELLED == "cancelled"
    
    def test_llm_provider_enum(self):
        """Test LLMProvider enum"""
        assert LLMProvider.OPENAI == "openai"
        assert LLMProvider.ANTHROPIC == "anthropic"
        assert LLMProvider.GOOGLE == "google"
        assert LLMProvider.HUGGINGFACE == "huggingface"
        assert LLMProvider.LOCAL == "local"
    
    def test_container_status_enum(self):
        """Test ContainerStatus enum"""
        assert ContainerStatus.CREATED == "created"
        assert ContainerStatus.RUNNING == "running"
        assert ContainerStatus.COMPLETED == "completed"
        assert ContainerStatus.FAILED == "failed"
        assert ContainerStatus.STOPPED == "stopped"
    
    def test_node_type_enum(self):
        """Test NodeType enum"""
        assert NodeType.TARGET == "target"
        assert NodeType.SESSION == "session"
        assert NodeType.VULNERABILITY == "vulnerability"
        assert NodeType.CREDENTIAL == "credential"
        assert NodeType.WORKFLOW == "workflow"
    
    def test_safety_level_enum(self):
        """Test SafetyLevel enum"""
        assert SafetyLevel.LOW == "low"
        assert SafetyLevel.MEDIUM == "medium"
        assert SafetyLevel.HIGH == "high"
        assert SafetyLevel.CRITICAL == "critical"
    
    def test_log_level_enum(self):
        """Test LogLevel enum"""
        assert LogLevel.DEBUG == "debug"
        assert LogLevel.INFO == "info"
        assert LogLevel.WARNING == "warning"
        assert LogLevel.ERROR == "error"
        assert LogLevel.CRITICAL == "critical"
    
    def test_event_type_enum(self):
        """Test EventType enum"""
        assert EventType.SYSTEM_START == "system_start"
        assert EventType.SYSTEM_SHUTDOWN == "system_shutdown"
        assert EventType.TARGET_CREATE == "target_create"
        assert EventType.WORKFLOW_CREATE == "workflow_create"
        assert EventType.PLUGIN_LOAD == "plugin_load"
        assert EventType.SECURITY_ALERT == "security_alert"


if __name__ == "__main__":
    pytest.main([__file__])