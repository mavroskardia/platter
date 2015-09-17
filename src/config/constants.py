# Numeric constants

gravity = 2.0
air_friction_x = 0.95
air_friction_y = 0.9
base_friction = 0.99

# Systems -- Core

SdlInitSystem = '.systems.sdlcore.SdlInitSystem'
SdlWindowSystem = '.systems.sdlcore.SdlWindowSystem'
InputSystem = '.systems.input.InputSystem'

# Systems -- Physical

Gravity = '.systems.physical.GravitySystem'
Jumping = '.systems.physical.JumpingSystem'
Force = '.systems.physical.ForceSystem'
CollisionDetection = '.systems.physical.CollisionDetectionSystem'
PositionUpdate = '.systems.physical.PositionUpdateSystem'
PlayerInput = '.systems.player.PlayerInputSystem'
Hud = '.systems.hud.HudSystem'
Map = '.systems.map.MapSystem'
SpriteSystem = '.systems.sprite.SpriteSystem'

# Systems -- Debugging

BorderRenderer = '.systems.decorations.BorderRendererSystem'

# Components -- Physical
Acceleration = '.components.physical.Acceleration'
AffectedByGravity = '.components.physical.AffectedByGravity'
CanCollide = '.components.physical.CanCollide'
PlayerControl = '.components.player.PlayerControl'
Body = '.components.physical.Body'
Text = '.components.hud.Text'
Sprite = '.components.sprite.Sprite'

# Components -- Debugging

Bordered = '.components.decoration.Bordered'
