# Helm Installation Guide for Windows

## Method 1: Using Chocolatey (Recommended)

```cmd
choco install kubernetes-helm
```

## Method 2: Using Scoop

```cmd
scoop install helm
```

## Method 3: Manual Installation

1. Download Helm from: https://github.com/helm/helm/releases
2. Download `helm-v3.x.x-windows-amd64.zip`
3. Extract the zip file
4. Move `helm.exe` to `C:\Program Files\helm\`
5. Add `C:\Program Files\helm\` to PATH:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Edit "Path" → Add new entry: `C:\Program Files\helm\`
6. Restart terminal

## Verify Installation

```cmd
helm version
```

## After Installation

```cmd
helm create todo-chat-bot
```

---

## Quick Install (if you have Chocolatey):

```cmd
choco install kubernetes-helm -y
```

Then restart your terminal and run:
```cmd
helm create todo-chat-bot
```
