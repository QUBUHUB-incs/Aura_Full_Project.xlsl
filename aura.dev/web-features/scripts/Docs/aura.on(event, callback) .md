---

#### 5. `feature-toggles.md`
```markdown
# Feature Toggles

Aura uses feature toggles for progressive enhancement and controlled rollout.

## Adding a New Feature
```js
aura.register("darkMode", {
  init() {
    document.body.classList.toggle("dark-mode")
  }
})
