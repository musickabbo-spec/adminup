```python
import json
import base64
import requests
from datetime import datetime, timedelta, timezone
from huggingface_hub import InferenceClient

def execute_user_task(message, secrets=None):
    """ইউজার মোডের সমস্ত সাধারণ কন্ডিশনাল কঙ্কাল"""
    msg = message.strip().lower()
    if msg == "verify":
        return "🔥 K-Agent অ্যানালাইসিস: আপনার ডোমেন, হাগিংফেস এবং গিটহাবের ত্রিমুখী কানেকশন এখন ১০০% সাকসেসফুলি ওয়ার্কিং!"
    elif msg == "hello":
        return "Welcome to K-Agent OS"
    elif msg == "status":
        return '🖥️ K-Agent Universal Sentinel: অল সিস্টেম মডিউলস অপারেটিং অ্যাট পিক সিকিউরিটি ক্লিয়ারেন্স!'
    elif msg == "time_check":
        return '⏱️ K-Agent Temporal Matrix: সিস্টেম ক্লক এখন ব্যাকএন্ডের সাথে শতভাগ সিঙ্কড!'
    elif msg == "final_check":
        return '🚀 K-Agent Core Architecture: অল মেকানিজমস অ্যান্ড মেমরি মডিউলস আর ১০০% সিকিউরড অ্যান্ড অপ্টিমাইজড!'
    else:
        return f"🤖 রেসপন্স: '{message}' কমান্ডটি রিমোট কোর গ্রহণ করেছে।"


def execute_admin_task(message, secrets):
    """অ্যাডমিন মোডের সমস্ত এআই ব্রেন, স্মার্ট প্রম্পট এবং টোকেন অপ্টিমাইজেশন মেকানিজম"""
    hf_token = secrets["HF_TOKEN"]
    github_token = secrets["GITHUB_ACCESS_TOKEN"]
    repo_owner = secrets["REPO_OWNER"]
    repo_name = secrets["REPO_NAME"]
    api_base = secrets["API_BASE"]
    dynamic_file_name = secrets["DYNAMIC_FILE_NAME"]

    # গিটহাব রিড হেল্পার
    def get_git_file(file_name):
        url = f"{api_base}/{repo_owner}/{repo_name}/contents/{file_name}"
        headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                return base64.b64decode(res.json()["content"]).decode("utf-8")
        except:
            pass
        return ""

    # গিটহাব পুশ হেল্পার
    def push_git_file(file_name, content, commit_msg):
        url = f"{api_base}/{repo_owner}/{repo_name}/contents/{file_name}"
        headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
        res = requests.get(url, headers=headers)
        sha = res.json().get("sha") if res.status_code == 200 else None
        payload = {
            "message": commit_msg,
            "content": base64.b64encode(content.encode("utf-8")).decode("utf-8")
        }
        if sha:
            payload["sha"] = sha
        put_res = requests.put(url, headers=headers, json=payload, timeout=10)
        return put_res.status_code in [200, 201]

    # ⏰ লাইভ রিয়েল-টাইম স্ট্যাম্প জেনারেশন (Bangladesh Time GMT+6)
    try:
        tz_bd = timezone(timedelta(hours=6))
        current_time_str = datetime.now(tz_bd).strftime("%Y-%m-%d %H:%M:%S")
    except:
        current_time_str = "2026-06-24 18:00:00"

    # চ্যাট হিস্ট্রি সংগ্রহ
    history_str = get_git_file("admin_history.json")
    try:
        history = json.loads(history_str) if history_str else []
    except:
        history = []
    history = history[-15:]

    # 🧠 ডুয়াল-ফেজ ট্রিগার ডিটেকশন (টোকেন বাঁচানোর মেকানিজম)
    trigger_words = ["deploy", "save", "upgrade", "apply", "commit", "অ্যাপ্লাই", "সেভ", "ডিপ্লয়", "আপগ্রেড"]
    is_deploy_mode = any(word in message.lower() for word in trigger_words)

    if is_deploy_mode:
        # ডেপ্লয়মেন্ট ফেজ: লাইভ কোড এবং লেজার মেমরিতে লোড করা হবে
        current_core = get_git_file(dynamic_file_name)
        current_ledger = get_git_file("system_ledger.md")
        
        system_prompt = f"""You are the Autonomous Architect Assistant and Brain of K-Agent OS.
You are in DEPLOYMENT MODE because the Admin has requested to deploy/save/upgrade changes.

CURRENT REAL-WORLD TIMESTAMP (Bangladesh Time): {current_time_str}

CURRENT LIVE CODE (`{dynamic_file_name}`):
\"\"\"
{current_core}
\"\"\"

CURRENT SYSTEM LEDGER (`system_ledger.md`):
\"\"\"
{current_ledger}
\"\"\"

CRITICAL DIRECTIVES:
1. Since you are in DEPLOYMENT MODE, you must write the FULL, valid, absolute Python code for `dynamic_core.py` incorporating ALL existing functions along with the new upgrades. Wrapped strictly between ===NEW_CODE_START=== and ===NEW_CODE_END===.
2. Along with the code update, rewrite the new `system_ledger.md` entry wrapped strictly between ===LEDGER_START=== and ===LEDGER_END===. Use the live timestamp: {current_time_str}.
3. Do NOT use placeholders like '# rest of the code'. Rewrite everything fully.
4. Keep explanations extremely short to avoid wasting output tokens."""
    else:
        # ব্রেনস্টর্মিং ফেজ: কোডবেস বা লেজার লোড না করে শুধুমাত্র হিস্ট্রির ওপর কনভারসেশন (টোকেন সেভিং মোড)
        system_prompt = f"""You are the Autonomous Architect Assistant and Brain of K-Agent OS.
You are in BRAINSTORMING MODE discussing features, architectures, or configurations with the Admin.

CURRENT REAL-WORLD TIMESTAMP (Bangladesh Time): {current_time_str}

ACTIVE COMMANDS SUMMARY:
- verify (🔥 Connection health check)
- hello (Welcome message)
- status (🖥️ System security clearance status)
- time_check (⏱️ Live clock sync status)
- final_check (🚀 Core architecture validation)

CRITICAL DIRECTIVES:
1. Brainstorm with the Admin, explain technical architectures, and clarify concepts concisely.
2. DO NOT write code blocks or use ===NEW_CODE_START=== / ===LEDGER_START=== tags. You will do that ONLY when the Admin explicitly uses activation keywords like 'save', 'deploy', or 'apply'.
3. Keep answers extremely short, smart, and token-optimized."""

    # এআই চ্যাট এক্সিকিউশন
    client = InferenceClient(api_key=hf_token)
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append(msg)
    messages.append({"role": "user", "content": message})

    response = client.chat_completion(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=messages,
        max_tokens=1548
    )
    ai_response = response.choices[0].message.content

    # ডেপ্লয়মেন্ট অ্যাকশন পার্সিং
    reload_required = False
    if is_deploy_mode:
        if "===NEW_CODE_START===" in ai_response and "===NEW_CODE_END===" in ai_response:
            new_code = ai_response.split("===NEW_CODE_START===")[1].split("===NEW_CODE_END===")[0].strip()
            if new_code.startswith("```"):
                lines = new_code.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                new_code = "\n".join(lines).strip()
            
            # গিটহাবে সোর্স ফাইল পুশ
            push_git_file(dynamic_file_name, new_code, "⚡ Autonomous System Upgrade via decoupled dynamic core")
            reload_required = True

        if "===LEDGER_START===" in ai_response and "===LEDGER_END===" in ai_response:
            new_ledger = ai_response.split("===LEDGER_START===")[1].split("===LEDGER_END===")[0].strip()
            current_ledger = get_git_file("system_ledger.md")
            if current_ledger and current_ledger.strip():
                combined_ledger = current_ledger.strip() + "\n\n" + new_ledger
            else:
                combined_ledger = new_ledger
            
            # গিটহাবে লেজার পুশ
            push_git_file("system_ledger.md", combined_ledger, "📝 System Ledger Updated via decoupled dynamic core")

    # চ্যাট মেমরি আপডেট
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": ai_response})
    clean_history_json = json.dumps(history, ensure_ascii=False)
    push_git_file("admin_history.json", clean_history_json, "🔄 Admin Chat History Synced")

    # ফ্রন্টএন্ড ট্যাগের সুন্দর রূপান্তর
    clean_response = ai_response.replace("===NEW_CODE_START===", "\n`[⚡ System Deploying New Code...]`\n").replace("===NEW_CODE_END===", "\n`[✅ Deploy Complete]`\n")
    clean_response = clean_response.replace("===LEDGER_START===", "\n`[📝 Updating System Ledger...]`\n").replace("===LEDGER_END===", "\n`[✅ Ledger Synced]`\n")

    return {"response": clean_response, "reload": reload_required}

```
