'use client';

import { useEffect, useState } from 'react';

export default function Home() {
  const [msg, setMsg] = useState('');

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    fetch(`${apiUrl}/ping`)
        .then(res => res.json())
        .then(data => setMsg(data.message));
  }, []);

  return (
    <main>
      <h1>If the message below includes "PONG", then you're basically ok.</h1>
      <p>{msg}</p>
    </main>
  );
}