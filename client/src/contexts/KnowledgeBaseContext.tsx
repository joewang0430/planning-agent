"use client";

import React, { createContext, useContext, useState, ReactNode, useEffect } from "react";
import { KnowledgeBaseFile } from "@/data/contentTypes";

interface KnowledgeBaseContextType {
    selectedKbList: KnowledgeBaseFile[];
    addKb: (kb: KnowledgeBaseFile) => void;
    removeKb: (kbName: string) => void;
};

const KnowledgeBaseContext = createContext<KnowledgeBaseContextType | undefined>(undefined);

const LOCAL_STORAGE_KEY = 'planning_agent_selected_kb';

interface KnowledgeBaseProviderProps {
    children: ReactNode;
};

export function KnowledgeBaseProvider({ children }: KnowledgeBaseProviderProps) {
    // The initial state is an empty array when both the server and the client render for the first time, ensuring consistency in hydration
    const [selectedKbList, setSelectedKbList] = useState<KnowledgeBaseFile[]>([]);

    // Load data from localStorage after the component is first mounted to the client
    useEffect(() => {
        try {
            const item = window.localStorage.getItem(LOCAL_STORAGE_KEY);
            if (item) {
                setSelectedKbList(JSON.parse(item));
            }
        } catch (error) {
            console.error("从 localStorage 读取知识库列表失败", error);
        }
    }, []); // Run only once when the client is mounted

    // When the selectedKbList changes, synchronize it to localStorage
    useEffect(() => {
        try {
            window.localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(selectedKbList));
        } catch (error) {
            console.error("向 localStorage 写入知识库列表失败", error);
        }
    }, [selectedKbList]);

    const addKb = (kb: KnowledgeBaseFile) => {
        setSelectedKbList(prev => prev.some(item => item.name === kb.name && item.category === kb.category) ? prev : [...prev, kb]);
    };

    const removeKb = (kbName: string) => {
        setSelectedKbList(prev => prev.filter(item => item.name !== kbName));
    };

    return (
        <KnowledgeBaseContext.Provider value={{ selectedKbList, addKb, removeKb }}>
            {children}
        </KnowledgeBaseContext.Provider>
    );
};

export function useKnowledgeBase() {
    const context = useContext(KnowledgeBaseContext);
    if (!context) throw new Error("useKnowledgeBase必须在KnowledgeBaseProvider中使用");
    return context;
};

