"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";
import { KnowledgeBaseFile } from "@/data/contentTypes";

interface KnowledgeBaseContextType {
    selectedKbList: KnowledgeBaseFile[];
    addKb: (kb: KnowledgeBaseFile) => void;
    removeKb: (kbName: string) => void;
};

const KnowledgeBaseContext = createContext<KnowledgeBaseContextType | undefined>(undefined);

interface KnowledgeBaseProviderProps {
    children: ReactNode;
};

export function KnowledgeBaseProvider({ children }: KnowledgeBaseProviderProps) {
    const [selectedKbList, setSelectedKbList] = useState<KnowledgeBaseFile[]>([]);

    const addKb = (kb: KnowledgeBaseFile) => {
        setSelectedKbList(prev => prev.some(item => item.name === kb.name) ? prev : [...prev, kb]);
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
