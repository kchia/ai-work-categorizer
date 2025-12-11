async def execute_tool_calls(tool_calls):
    results = []
    for call in tool_calls:
        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                execute_single_tool(call),
                timeout=30.0  # 30 sec max per tool
            )
            results.append({"status": "success", "result": result})
        except asyncio.TimeoutError:
            results.append({
                "status": "timeout",
                "error": f"Tool {call['function']} timed out",
                "fallback": "Queued for retry"
            })
        except APIError as e:
            if e.status_code == 429:  # Rate limit
                results.append({
                    "status": "rate_limited",
                    "retry_after": e.retry_after,
                    "fallback": "Queued with exponential backoff"
                })
            else:
                results.append({
                    "status": "error",
                    "error": str(e),
                    "fallback": "Flagged for human review"
                })
    return results
