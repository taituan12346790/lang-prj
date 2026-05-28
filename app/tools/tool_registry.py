# app/tools/tool_registry.py
import asyncio
from typing import Dict, Any, Callable
from loguru import logger


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        """Đăng ký tool (thường là wrapper.execute)"""
        if callable(func):
            self.tools[name] = func
            logger.info(f"✅ Tool registered: {name}")
        else:
            logger.error(f"❌ Cannot register {name}: not callable")

    async def execute(self, tool_name: str, params: Dict[str, Any]) -> Dict:
        """
        Chạy tool theo tên
        """
        if tool_name not in self.tools:
            logger.error(f"❌ Tool not found: {tool_name}")
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "data": None
            }

        tool_func = self.tools[tool_name]

        try:
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(params)
            else:
                result = await asyncio.to_thread(tool_func, params)

            # Chuẩn hóa output
            if isinstance(result, dict) and "success" not in result:
                return {"success": True, "data": result}
            return result

        except Exception as e:
            logger.exception(f"Error executing tool '{tool_name}'")
            return {
                "success": False,
                "error": f"Execution failed: {str(e)}",
                "data": None
            }
    def get_tool(self, name: str):
        """Lấy tool đã đăng ký theo tên"""
        return self.tools.get(name)

# Global instance
tool_registry = ToolRegistry()
