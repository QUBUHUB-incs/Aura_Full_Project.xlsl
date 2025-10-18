**markdown**
---

#### 4. `events.md`
```markdown
# Event System — Aura Scripts

Aura’s event bus allows seamless interaction between UI features and the AI brain.

| Event | Description |
|--------|-------------|
| `onAuraReady` | Triggered when all scripts are initialized |
| `onFeatureLoad` | Fired after a feature script loads |
| `onAIResponse` | Triggered when the AI layer sends data to the frontend |
| `onVoiceCommand` | Fired on successful speech recognition |

Example:
```js
aura.on("onAIResponse", (data) => console.log("AI:", data))
