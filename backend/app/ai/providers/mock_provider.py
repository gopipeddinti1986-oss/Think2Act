from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from app.ai.providers.base import BaseAIProvider, AIProviderResponse, AIToolCall

class MockAIProvider(BaseAIProvider):
    async def generate_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> AIProviderResponse:
        user_message = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                user_message = m.get("content", "")
                break

        msg_lower = user_message.lower()
        ctx = context or {}
        tasks_summary = ctx.get("tasks_summary", {})
        recent_tasks = ctx.get("recent_tasks", [])
        skills = ctx.get("skills", [])
        pending_count = tasks_summary.get("pending", 0)

        tool_calls: List[AIToolCall] = []

        # Intent 1: Planning / Prioritization / What to do today
        if any(w in msg_lower for w in ["what should i do", "what to do", "plan today", "prioritize", "schedule"]):
            if pending_count > 0 and recent_tasks:
                top_task = recent_tasks[0]
                now = datetime.now(timezone.utc)
                start_slot = now + timedelta(hours=1)
                end_slot = start_slot + timedelta(minutes=45)

                content = (
                    f"Based on your current execution workload, you have **{pending_count} pending tasks**. "
                    f"I recommend tackling **'{top_task['title']}'** ({top_task.get('priority', 'MEDIUM')} Priority) during your peak focus window."
                )
                if skills:
                    lowest_skill = sorted(skills, key=lambda s: s.get("level", 0))[0]
                    content += f" Also, your **{lowest_skill.get('name', 'Core')}** skill is currently at {lowest_skill.get('level', 0)}/100, which provides high career leverage."

                tool_calls.append(AIToolCall(
                    name="schedule_task",
                    arguments={
                        "task_id": top_task["id"],
                        "task_title": top_task["title"],
                        "start_at": start_slot.isoformat(),
                        "end_at": end_slot.isoformat(),
                        "reason": f"Priority execution block ({top_task.get('priority', 'MEDIUM')})"
                    }
                ))
            else:
                content = (
                    "All your scheduled tasks are currently clear! To maintain momentum, "
                    "I suggest creating a focused practice task targeting your core skill roadmap."
                )
                tool_calls.append(AIToolCall(
                    name="create_task",
                    arguments={
                        "title": "Solve 3 Graph & Tree Algorithmic Problems",
                        "description": "Strengthen DSA evidence for technical interview preparation",
                        "priority": "HIGH",
                        "estimated_minutes": 60,
                        "category": "DSA"
                    }
                ))

        # Intent 2: Learning / Create task / Study
        elif any(w in msg_lower for w in ["learn", "create task", "add task", "study"]):
            topic = "SQL Optimization" if "sql" in msg_lower else "Docker Deployment" if "docker" in msg_lower else "System Architecture"
            content = (
                f"I've structured a high-impact learning challenge for **{topic}**. "
                f"Completing this will add verified project evidence to your Skill Graph."
            )
            tool_calls.append(AIToolCall(
                name="create_task",
                arguments={
                    "title": f"Complete hands-on {topic} workshop & implementation",
                    "description": f"Practical exercise to close verified skill gap in {topic}",
                    "priority": "HIGH",
                    "estimated_minutes": 60,
                    "category": "Learning"
                }
            ))

        # Intent 3: Create Goal
        elif any(w in msg_lower for w in ["create goal", "add goal", "new goal", "target"]):
            content = "I've structured a target career milestone for your development."
            tool_calls.append(AIToolCall(
                name="create_goal",
                arguments={
                    "title": "Master Backend Microservices Architecture",
                    "description": "Demonstrate proficiency in asynchronous processing and distributed patterns",
                    "category": "Career",
                    "priority": "HIGH"
                }
            ))

        # Intent 4: Productivity / Progress review
        elif any(w in msg_lower for w in ["productivity", "progress", "performance", "how am i doing", "focus", "accomplish", "done today"]):
            total = tasks_summary.get("total", 0)
            completed = tasks_summary.get("completed", 0)
            rate = tasks_summary.get("rate", 0)
            focus_m = ctx.get("today_focus_mins", 0)
            content = (
                f"📊 **Performance Snapshot:**\n\n"
                f"- **Task Completion Rate:** {rate}% ({completed}/{total} tasks)\n"
                f"- **Today's Focus Time:** {focus_m} minutes logged\n\n"
                f"You have completed {completed} task{'s' if completed != 1 else ''} and logged {focus_m} minutes of focus today. "
                f"Your execution is steady."
            )

        # General Coaching & Feedback
        else:
            skills_summary = ", ".join([f"{s.get('name', 'Skill')} ({s.get('level', 0)}/100)" for s in skills[:3]]) if skills else "General Software Engineering"
            content = (
                f"I'm observing your system state: your tracked skills include **{skills_summary}**, "
                f"with **{pending_count} pending tasks** today.\n\n"
                f"How would you like to direct your energy today? I can help you plan time blocks, close specific skill gaps, or schedule focused execution sprints."
            )

        return AIProviderResponse(content=content, tool_calls=tool_calls)
