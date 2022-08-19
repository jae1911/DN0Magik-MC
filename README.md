# DN0Magik-MC
The DN0Magik Minecraft auth &amp; skins server

## Goals

The goals of the projects are:
 - To create a [Mojang-API](https://wiki.vg/Mojang_API) compatible solution
 - Easily self-hostable
 - IPv6-ready
 - Integration with existing Minecraft skins
 - Fully Open-Source

### Working

 - Register (`/api/v1/register`)
 - Login (`/authenticate`)
 - Profile display (`/minecraft/profile`)
 - Token refresh (`/refresh`)
 - Status check (`/check`)
 - Sales stats (`/orders/statistics`)
 - Get active capes (`/minecraft/profile/capes/active`)
 - Get active skins (`/minecraft/profile/skins/active`)
 - Upload skin (`/minecraft/profile/skins`)

### TODO

 - Skin API
 - AuthLib modification (for new authentication to work within the game itself)
