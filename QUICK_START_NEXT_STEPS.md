# QUICK START: Next Steps (3 Simple Actions)

## What You Need To Do Right Now

### Action 1: Update Render Backend Environment Variables (5 min)

1. Go to: https://dashboard.render.com/services
2. Click your **backend service** (lang-prj-backend)
3. Go to **Settings** tab
4. Scroll to **Environment Variables** section
5. Update these 4 variables:

```
GROQ_API_KEY = (use key provided in email/chat - never commit)
FRONTEND_URL = https://lang-prj.onrender.com
BACKEND_URL = https://lang-prj-backend.onrender.com
ENVIRONMENT = production
```

6. Click **Save** (it will auto-redeploy)
7. Wait 2-3 minutes for deployment to complete


### Action 2: Update Google Cloud Console (2 min)

1. Go to: https://console.cloud.google.com/apis/credentials
2. Find your OAuth 2.0 Client ID (Web application)
3. Click **Edit** (pencil icon)
4. In **Authorized redirect URIs**, add:
   ```
   https://lang-prj-backend.onrender.com/api/auth/google/callback
   ```
5. Remove old URIs (like `ai-language-tutor-frontend.onrender.com`)
6. Click **Save**


### Action 3: Test It (2 min)

1. Open https://lang-prj.onrender.com in new browser
2. Click **"Đăng nhập bằng Google"** button
3. Complete Google login
4. After Google auth, should see your dashboard ✅
5. Try chatting with AI - should work

---

## ⚠️ If Something Doesn't Work

| Problem | Solution |
|---------|----------|
| Still redirects to old URL after Google login | Check that `FRONTEND_URL` is exactly `https://lang-prj.onrender.com` on Render |
| OAuth button leads to error page | Verify Google Cloud Console has correct redirect URI |
| Chat shows "model decommissioned" error | Check `GROQ_API_KEY` is updated correctly |
| Chat doesn't respond | Check Render logs for errors |
| Onboarding appears instead of dashboard | Normal for first Google login, complete language setup |

---

## 📋 Full Details

For complete information, see: **`RENDER_ENV_UPDATE_CHECKLIST.md`**

For session summary, see: **`CURRENT_SESSION_SUMMARY.md`**

---

## ✅ Code Status

- ✅ OAuth URL fixed in code
- ✅ Code committed to GitHub
- ✅ Ready for production deployment
- ⏳ Waiting for your Render dashboard update

---

**Estimated time to complete**: ~10 minutes  
**Complexity**: Easy (just copy-paste values)  
**Risk**: Low (just environment variables, no code changes)

Let me know when done and we can test! 🚀
