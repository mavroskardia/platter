# Numeric constants

gravity = 2.0
air_friction_x = 0.95
air_friction_y = 0.9
base_friction = 0.01

# Systems -- Core

Sdl = '.systems.sdl.SdlSystem'
Input = '.systems.input.InputSystem'

# Systems -- Physical

Physics = '.systems.physical.PhysicsSystem'
Gravity = '.systems.physical.GravitySystem'
Jumping = '.systems.physical.JumpingSystem'
Force = '.systems.physical.ForceSystem'
CollisionDetection = '.systems.physical.CollisionDetectionSystem'
PositionUpdate = '.systems.physical.PositionUpdateSystem'
PlayerInput = '.systems.player.PlayerInputSystem'
PlayerDataSystem = '.systems.player.PlayerDataSystem'
Hud = '.systems.hud.HudSystem'
Map = '.systems.map.MapSystem'
SpriteSystem = '.systems.sprite.SpriteSystem'

# Systems -- Debugging

BorderRenderer = '.systems.decorations.BorderRendererSystem'
VectorRenderer = '.systems.decorations.VectorRendererSystem'

# Components -- Physical

Acceleration = '.components.physical.Acceleration'
CanCollide = '.components.physical.CanCollide'
HasPhysics = '.components.physical.HasPhysics'
PlayerControl = '.components.player.PlayerControl'
PlayerData = '.components.player.PlayerData'
Body = '.components.physical.Body'
Text = '.components.hud.Text'
Sprite = '.components.sprite.Sprite'

# Components -- Debugging

Bordered = '.components.decoration.Bordered'
