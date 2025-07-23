"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

export const Plan = () => {
    const searchParams = useSearchParams();
    const title = searchParams.get('title') || '';
    const [data, setData] = useState<string | null>(null);

    useEffect(() => {
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/endpointTBD?title=${encodeURIComponent(title)}`)
            .then(res => res.json())
            .then(res => setData(res))
            .catch(() => setData(null))
    }, [title]);

    return (
        <>
            <h2>专项规划详情</h2>
            <div>标题: {title}</div>
            <div>API结果: {data ? JSON.stringify(data) : "加载中..."}</div>
        </>
    );
};