# 🗄️ MongoDB Setup Guide

You have **two options** for setting up MongoDB. Choose the one that works best for you.

---

## ✅ Option 1: MongoDB Atlas (Cloud - FASTEST) ☁️

**Recommended for quick start - no local installation needed!**

### Step 1: Create Free MongoDB Atlas Account

1. Go to [mongodb.com/cloud/atlas/register](https://mongodb.com/cloud/atlas/register)
2. Sign up for a free account
3. Choose the **FREE tier** (M0 Sandbox)

### Step 2: Create a Cluster

1. After logging in, click **"Build a Database"**
2. Choose **FREE** tier (M0)
3. Select a cloud provider and region (closest to you)
4. Click **"Create Cluster"** (takes 3-5 minutes)

### Step 3: Create Database User

1. Click **"Database Access"** in the left sidebar
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Username: `admin` (or your choice)
5. Password: Create a strong password (save it!)
6. User Privileges: **"Atlas admin"**
7. Click **"Add User"**

### Step 4: Allow Network Access

1. Click **"Network Access"** in the left sidebar
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (for development)
   - This adds `0.0.0.0/0` (use with caution in production)
4. Click **"Confirm"**

### Step 5: Get Connection String

1. Go back to **"Database"** → Click **"Connect"**
2. Choose **"Connect your application"**
3. Driver: **Python**, Version: **3.12 or later**
4. Copy the connection string, it looks like:
   ```
   mongodb+srv://admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### Step 6: Update .env File

1. Open `.env` file in your project
2. Replace `<password>` in the connection string with your actual password
3. Update the file:

```env
MONGODB_URI=mongodb+srv://admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=adaptive_test
OPENAI_API_KEY=your_openai_api_key_here
```

**Important**: Replace `YOUR_PASSWORD` with the password you created in Step 3!

### Step 7: Test Connection

```bash
python seed_questions.py
```

You should see:
```
✅ Successfully inserted 15 questions
```

---

## ✅ Option 2: Local MongoDB Installation (Windows)

**For development without internet dependency**

### Step 1: Download MongoDB

1. Go to [mongodb.com/try/download/community](https://mongodb.com/try/download/community)
2. Version: **7.0 or later**
3. Platform: **Windows x64**
4. Package: **MSI**
5. Click **"Download"**

### Step 2: Install MongoDB

1. Run the downloaded `.msi` file
2. Choose **"Complete"** installation
3. **Important**: Check **"Install MongoDB as a Service"**
4. Check **"Install MongoDB Compass"** (GUI tool - optional but helpful)
5. Click **"Next"** → **"Install"**

### Step 3: Verify Installation

```powershell
# Check if MongoDB service is running
Get-Service MongoDB

# Should show: Status = Running
```

If not running, start it:
```powershell
net start MongoDB
```

### Step 4: Verify Connection

Your `.env` file should already have:
```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=adaptive_test
```

Test it:
```bash
python seed_questions.py
```

---

## 🎯 Quick Comparison

| Feature | MongoDB Atlas ☁️ | Local MongoDB 💻 |
|---------|-----------------|------------------|
| Setup Time | 5 minutes | 10-15 minutes |
| Internet Required | Yes | No |
| Installation | None | ~500 MB download |
| Free Tier | 512 MB storage | Unlimited |
| Best For | Quick start, deployment | Development offline |

---

## 🧪 Testing Your Connection

After setting up either option, test with:

```bash
# Seed the database
python seed_questions.py
```

**Success output:**
```
✅ Successfully inserted 15 questions

Questions by difficulty:
  Easy (0.1-0.3): 4
  Medium (0.4-0.6): 5
  Hard (0.7-0.9): 6

Questions by topic:
  Arithmetic: 6
  Algebra: 6
  Geometry: 2
  Calculus: 2
```

---

## 🐛 Troubleshooting

### MongoDB Atlas Issues

**Problem**: Connection timeout
```
ServerSelectionTimeoutError
```

**Solutions**:
1. Check Network Access allows your IP (`0.0.0.0/0`)
2. Verify password in connection string (no special chars issues)
3. Check cluster is fully created (green status)
4. Ensure connection string includes `retryWrites=true&w=majority`

**Problem**: Authentication failed
```
Authentication failed
```

**Solutions**:
1. Double-check username and password
2. Make sure password in `.env` matches the one you created
3. URL encode special characters in password:
   - `@` → `%40`
   - `#` → `%23`
   - `$` → `%24`

### Local MongoDB Issues

**Problem**: Service won't start
```
net start MongoDB
# Error: service not found
```

**Solutions**:
1. Reinstall MongoDB with "Install as Service" checked
2. Or run MongoDB manually:
   ```powershell
   "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath "C:\data\db"
   ```

**Problem**: Connection refused
```
[WinError 10061] No connection could be made
```

**Solutions**:
1. Start MongoDB service: `net start MongoDB`
2. Check if running: `Get-Service MongoDB`
3. Check port 27017 is not in use: `netstat -an | findstr 27017`

---

## ✅ Next Steps

Once MongoDB is set up and `seed_questions.py` runs successfully:

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Test the API**:
   ```bash
   python test_api.py
   ```

3. **Visit interactive docs**:
   ```
   http://localhost:8000/docs
   ```

---

## 🚀 For Deployment

When deploying to Render/Railway/Fly.io:
- **Use MongoDB Atlas** (not local MongoDB)
- Set `MONGODB_URI` as environment variable in your deployment platform
- The cloud database will work from anywhere

---

## 📚 Resources

- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [MongoDB Installation Guide](https://docs.mongodb.com/manual/installation/)
- [Connection String Format](https://docs.mongodb.com/manual/reference/connection-string/)

---

**Need help?** Open an issue or check the troubleshooting section above.
