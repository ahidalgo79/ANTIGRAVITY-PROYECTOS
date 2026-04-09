"""Cliente MCP simplificado para conectar con servidores locales/remotos"""
import asyncio
import json
from typing import Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self, server_command: str, server_args: list[str] = None):
        self.server_command = server_command
        self.server_args = server_args or []
        self.session: Optional[ClientSession] = None
    
    async def connect(self):
        """Establece conexión con el servidor MCP"""
        params = StdioServerParameters(
            command=self.server_command,
            args=self.server_args,
            env=None
        )
        self._stdio_context = stdio_client(params)
        self._read, self._write = await self._stdio_context.__aenter__()
        self.session = ClientSession(self._read, self._write)
        await self.session.initialize()
        return self
    
    async def call_tool(self, tool_name: str, arguments: dict = None) -> Any:
        """Ejecuta una herramienta del servidor MCP"""
        result = await self.session.call_tool(tool_name, arguments or {})
        return result.content
    
    async def list_tools(self) -> list:
        """Lista herramientas disponibles en el servidor"""
        tools = await self.session.list_tools()
        return [t.name for t in tools.tools]
    
    async def close(self):
        """Cierra la conexión"""
        if self.session:
            await self.session.close()
        if hasattr(self, '_stdio_context'):
            await self._stdio_context.__aexit__(None, None, None)

# Helper para uso sincrónico (más simple para empezar)
def mcp_call(server: str, tool: str, args: dict = None) -> Any:
    """Llamada MCP sincrónica (wrapper sobre async)"""
    import subprocess, json
    
    # Ejemplo: conectar con notebooklm-server via stdio
    if server == "notebooklm":
        cmd = ["npx", "-y", "@anthropic-ai/notebooklm-mcp-server"]
    else:
        raise ValueError(f"Servidor MCP no configurado: {server}")
    
    # Ejecutar y capturar output (simplificado para demo)
    try:
        proc = subprocess.run(
            cmd + [json.dumps({"tool": tool, "args": args or {}})],
            capture_output=True, text=True, timeout=30
        )
        return json.loads(proc.stdout) if proc.stdout else {"error": proc.stderr}
    except Exception as e:
        return {"error": str(e)}