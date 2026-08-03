# interface/render_ui.py
import pygame
from config import WINDOW_WIDTH, UI_WIDTH_PIXELS, TOP_UI_HEIGHT, VIEWPORT_WIDTH,WINDOW_HEIGHT

from ecs.components.health import Health
from ecs.components.hunger import Hunger
from ecs.components.inventory import Inventory
from ecs.components.type import Type
# Assuming you have a Job/Jobs component based on your request. Adjust import as needed.
from ecs.components.job import Job 

# Strict Component Mapping Dictionary
# Format: "Display Name": (ComponentClass, 'attribute_name', optional_max_value)
COMPONENTS = {
    "Type": (Type, 'type'),
    "Health": (Health, 'health', 100),
    "Hunger": (Hunger, 'hunger', 100),
    "Inventory": (Inventory, 'items'),
    "Job": (Job, 'job')
}

def render_ui(screen, world, state, top_ui_height):
    font = pygame.font.SysFont(None, 24)
    font_small = pygame.font.SysFont(None, 18)
    
    # =============================================================
    # A. TOP BUTTON BAR
    # =============================================================
    top_bar_rect = pygame.Rect(0, 0, VIEWPORT_WIDTH, top_ui_height)
    pygame.draw.rect(screen, (50, 50, 50), top_bar_rect)
    pygame.draw.line(screen, (80, 80, 80), (0, top_ui_height), (VIEWPORT_WIDTH, top_ui_height), 2)
    
    # 1. Follow Button
    btn_color = (60, 160, 60) if state["is_follow_mode"] else (100, 100, 100)
    follow_btn_rect = pygame.Rect(20, 12, 130, 36)
    pygame.draw.rect(screen, btn_color, follow_btn_rect, border_radius=4)
    pygame.draw.rect(screen, (200, 200, 200), follow_btn_rect, 1, border_radius=4)
    txt_surf = font.render("Follow", True, (255, 255, 255))
    screen.blit(txt_surf, txt_surf.get_rect(center=follow_btn_rect.center))

    # 2. Pause Button
    pause_color = (180, 60, 60) if state["is_paused"] else (80, 80, 110)
    pause_btn_rect = pygame.Rect(160, 12, 120, 36)
    pygame.draw.rect(screen, pause_color, pause_btn_rect, border_radius=4)
    pygame.draw.rect(screen, (200, 200, 200), pause_btn_rect, 1, border_radius=4)
    pause_surf = font.render("Pause (SPC)", True, (255, 255, 255))
    screen.blit(pause_surf, pause_surf.get_rect(center=pause_btn_rect.center))

    # 3. Speed Control
    speed_btn_rect = pygame.Rect(290, 12, 90, 36)
    pygame.draw.rect(screen, (70, 70, 90), speed_btn_rect, border_radius=4)
    pygame.draw.rect(screen, (200, 200, 200), speed_btn_rect, 1, border_radius=4)
    speed_surf = font.render(f"Speed: {state['sim_speed']}x", True, (255, 255, 255))
    screen.blit(speed_surf, speed_surf.get_rect(center=speed_btn_rect.center))

    # =============================================================
    # B. RIGHT-HAND SIDEBAR (Inspector & Stats)
    # =============================================================
    sidebar_rect = pygame.Rect(VIEWPORT_WIDTH, 0, UI_WIDTH_PIXELS, WINDOW_HEIGHT)
    pygame.draw.rect(screen, (35, 35, 35), sidebar_rect)
    pygame.draw.line(screen, (80, 80, 80), (VIEWPORT_WIDTH, 0), (VIEWPORT_WIDTH, WINDOW_HEIGHT), 2)

    y_offset = 20

    # 1. Overlay Indicators
    overlay_header = font.render("OVERLAYS (F1-F4)", True, (100, 200, 220))
    screen.blit(overlay_header, (VIEWPORT_WIDTH + 20, y_offset))
    y_offset += 25

    overlays = [
        ("F1: Vision", state["show_vision"]),
        ("F2: Path", state["show_path"]),
        ("F3: Target", state["show_target"]),
        ("F4: Jobs", state["show_jobs"])
    ]
    
    for name, is_active in overlays:
        color = (100, 255, 100) if is_active else (150, 150, 150)
        surf = font_small.render(name, True, color)
        screen.blit(surf, (VIEWPORT_WIDTH + 20, y_offset))
        y_offset += 20
        
    y_offset += 10
    pygame.draw.line(screen, (70, 70, 70), (VIEWPORT_WIDTH + 10, y_offset), (WINDOW_WIDTH - 10, y_offset), 1)
    y_offset += 20

    # 2. Strict Component Inspector Panel
    inspector_header = font.render("COMPONENT INSPECTOR", True, (220, 220, 100))
    screen.blit(inspector_header, (VIEWPORT_WIDTH + 20, y_offset))
    y_offset += 30

    selected_entity = state["selected_entity"]

    # Use has_component for safety if entity_exists is not globally implemented
    if selected_entity is not None:
        id_surf = font_small.render(f"Selected ID: {selected_entity}", True, (255, 255, 255))
        screen.blit(id_surf, (VIEWPORT_WIDTH + 20, y_offset))
        y_offset += 25

        # Dictionary Driven Rendering
        for display_name, mapping in COMPONENTS.items():
            comp_class = mapping[0]
            attr_name = mapping[1]
            max_value = mapping[2] if len(mapping) > 2 else None

            if world.has_component(selected_entity, comp_class):
                comp_instance = world.get_component(selected_entity, comp_class)
                
                # Fetch the value safely
                val = getattr(comp_instance, attr_name, "N/A")

                comp_title = font_small.render(f"[{display_name}]", True, (150, 220, 150))
                screen.blit(comp_title, (VIEWPORT_WIDTH + 20, y_offset))
                y_offset += 20

                # Render a bar if a max_value was provided in the dictionary
                if max_value is not None and isinstance(val, (int, float)):
                    bar_width = 150
                    bar_height = 12
                    fill_pct = max(0.0, min(1.0, float(val) / float(max_value)))
                    
                    bar_bg = pygame.Rect(VIEWPORT_WIDTH + 30, y_offset + 3, bar_width, bar_height)
                    bar_fill = pygame.Rect(VIEWPORT_WIDTH + 30, y_offset + 3, int(bar_width * fill_pct), bar_height)
                    
                    pygame.draw.rect(screen, (60, 60, 60), bar_bg)
                    
                    # Color logic based on what the stat is
                    bar_color = (200, 60, 60) if display_name == "Hunger" else (60, 200, 60)
                    pygame.draw.rect(screen, bar_color, bar_fill)
                    pygame.draw.rect(screen, (200, 200, 200), bar_bg, 1)
                    
                    attr_surf = font_small.render(f"  {attr_name}: {val}/{max_value}", True, (220, 220, 220))
                    screen.blit(attr_surf, (VIEWPORT_WIDTH + 30 + bar_width + 5, y_offset))
                else:
                    # Standard text render
                    attr_surf = font_small.render(f"  {attr_name}: {val}", True, (200, 200, 200))
                    screen.blit(attr_surf, (VIEWPORT_WIDTH + 30, y_offset))
                
                y_offset += 25
    else:
        none_surf = font_small.render("No entity selected. Click an entity.", True, (150, 150, 150))
        screen.blit(none_surf, (VIEWPORT_WIDTH + 20, y_offset))

    return {
        "follow_btn": follow_btn_rect,
        "pause_btn": pause_btn_rect,
        "speed_btn": speed_btn_rect
    }
