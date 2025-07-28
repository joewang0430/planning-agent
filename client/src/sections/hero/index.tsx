"use client";

import React, { useState } from 'react';
import BaseButtonHome from '@/components/home/BaseButtonHome';
import PlanningButtonHome from '@/components/home/PlanningButtonHome';

export default function Hero() {
  const [title, setTitle] = useState('');

  return (
    <div className="min-h-screen flex flex-col items-center justify-center hero-gradient-bg">
      <h1
        className="text-5xl font-medium mb-16 text-plagt-blue-1"
      >
        专项规划 Agent
      </h1>
      <div className="mb-3 text-base text-plagt-grey-txt" style={{ color: 'var(--plagt-grey-txt)' }}>
        请输入规划标题
      </div>
      <input
        type="text"
        value={title}
        onChange={e => setTitle(e.target.value)}
        placeholder="(部门/单位名称) + 关于 + (核心主题) + 的专项规划"
        className="w-[70vw] max-w-[800px] text-lg px-5 py-3 rounded-xl border mb-10 outline-none bg-white bg-opacity-95 text-gray-800 text-plagt-grey-txt"
      />
      <div className="flex flex-col sm:flex-row gap-4 sm:gap-8 w-full justify-center items-center">
        <BaseButtonHome />
        <PlanningButtonHome title={title} setTitle={setTitle}/>
      </div>
    </div>
  );
}