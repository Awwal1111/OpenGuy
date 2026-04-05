"""
visualizer.py - Convert robot state to visualization coordinates.
Simple 2D workspace visualization helpers.
"""

from typing import Dict, Any, Tuple


class Workspace2D:
    """Helper class for 2D workspace visualization."""
    
    def __init__(self, width: float = 200, height: float = 200, canvas_width: int = 400, canvas_height: int = 400):
        """
        Initialize 2D workspace.
        
        Args:
            width: Physical workspace width (cm)
            height: Physical workspace height (cm)
            canvas_width: Canvas width in pixels
            canvas_height: Canvas height in pixels
        """
        self.width = width
        self.height = height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
    
    def world_to_canvas(self, x: float, y: float) -> Tuple[int, int]:
        """Convert world coordinates to canvas coordinates."""
        # Center the workspace
        canvas_x = int((x + self.width / 2) / self.width * self.canvas_width)
        canvas_y = int((self.height / 2 - y) / self.height * self.canvas_height)  # Flip Y axis
        return canvas_x, canvas_y
    
    def get_robot_svg(self, robot_state: Dict[str, Any]) -> str:
        """Generate SVG visualizing the robot state."""
        x = robot_state.get('x', 0)
        y = robot_state.get('y', 0)
        facing = robot_state.get('facing', 0)
        gripper_open = robot_state.get('gripper_open', True)
        
        # Convert to canvas coordinates
        cx, cy = self.world_to_canvas(x, y)
        
        # Robot body (circle)
        robot_svg = f'<circle cx="{cx}" cy="{cy}" r="12" fill="#a8ff78" opacity="0.8"/>'
        
        # Direction indicator (line showing which way robot is facing)
        import math
        rad = math.radians(facing)
        ex = cx + 15 * math.cos(rad)
        ey = cy - 15 * math.sin(rad)
        robot_svg += f'<line x1="{cx}" y1="{cy}" x2="{int(ex)}" y2="{int(ey)}" stroke="#78ffd6" stroke-width="2"/>'
        
        # Gripper indicator
        gripper_color = "#a8ff78" if gripper_open else "#ff5a4a"
        gripper_label = "O" if gripper_open else "●"
        robot_svg += f'<text x="{cx}" y="{cy + 20}" text-anchor="middle" fill="{gripper_color}" font-size="12" font-weight="bold">{gripper_label}</text>'
        
        return robot_svg
    
    def get_grid_svg(self) -> str:
        """Generate SVG grid for workspace."""
        grid_svg = f'<rect x="0" y="0" width="{self.canvas_width}" height="{self.canvas_height}" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>'
        
        # Major gridlines every 50cm
        for i in range(0, int(self.width * 2), 50):
            x = int(i / self.width * self.canvas_width)
            if 0 <= x <= self.canvas_width:
                grid_svg += f'<line x1="{x}" y1="0" x2="{x}" y2="{self.canvas_height}" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>'
        
        for i in range(0, int(self.height * 2), 50):
            y = int(i / self.height * self.canvas_height)
            if 0 <= y <= self.canvas_height:
                grid_svg += f'<line x1="0" y1="{y}" x2="{self.canvas_width}" y2="{y}" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>'
        
        # Center crosshair
        cx = self.canvas_width // 2
        cy = self.canvas_height // 2
        grid_svg += f'<line x1="{cx-10}" y1="{cy}" x2="{cx+10}" y2="{cy}" stroke="rgba(120,255,214,0.3)" stroke-width="1"/>'
        grid_svg += f'<line x1="{cx}" y1="{cy-10}" x2="{cx}" y2="{cy+10}" stroke="rgba(120,255,214,0.3)" stroke-width="1"/>'
        
        return grid_svg
    
    def get_full_svg(self, robot_state: Dict[str, Any]) -> str:
        """Generate complete SVG visualization."""
        svg = f'''<svg width="{self.canvas_width}" height="{self.canvas_height}" viewBox="0 0 {self.canvas_width} {self.canvas_height}" style="background:rgba(19,19,22,0.5); border:1px solid rgba(255,255,255,0.1); border-radius:10px;">
          <defs>
            <style>
              text {{ font-family: 'DM Mono', monospace; font-size: 10px; }}
            </style>
          </defs>
          {self.get_grid_svg()}
          {self.get_robot_svg(robot_state)}
          <text x="10" y="20" fill="rgba(237,237,240,0.5)">X: {robot_state.get('x', 0):.1f}cm</text>
          <text x="10" y="35" fill="rgba(237,237,240,0.5)">Y: {robot_state.get('y', 0):.1f}cm</text>
          <text x="10" y="50" fill="rgba(237,237,240,0.5)">°: {robot_state.get('facing', 0):.0f}°</text>
        </svg>'''
        return svg


def get_workspace_visualization(robot_state: Dict[str, Any]) -> str:
    """Get 2D workspace visualization as SVG."""
    workspace = Workspace2D()
    return workspace.get_full_svg(robot_state)
