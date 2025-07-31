"use client";

import { useState } from 'react';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { KnowledgeBaseFile } from '@/data/contentTypes';

interface PolicyDisplayProps {
  policy: string;
  kb_list: KnowledgeBaseFile[];
}

const PolicyDisplay = ({ policy, kb_list = [] }: PolicyDisplayProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!policy) {
    return null;
  }

  const kbCount = kb_list.length;

  return (
    <div className="bg-gray-100 rounded-lg p-3 text-sm text-gray-700 mb-4 transition-all duration-300">
      <div 
        className="flex items-center cursor-pointer select-none"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        {isExpanded ? <ChevronDown size={18} className="mr-1 flex-shrink-0" /> : <ChevronRight size={18} className="mr-1 flex-shrink-0" />}
        <span className="font-medium text-gray-800 mr-2 flex-shrink-0">{isExpanded ? '收起' : '展开'}</span>
        
        {/* Folded */}
        {!isExpanded && (
          <div className="flex-1 min-w-0">
            <p className="truncate text-gray-600">
              已参考 {kbCount} 个知识库，展开查看详情
            </p>
          </div>
        )}
      </div>
      
      {/* Expanded */}
      {isExpanded && (
        <div className="mt-2 pl-6 animate-fade-in">
          <div className="mb-4">
            <h4 className="font-semibold text-gray-800 mb-2">
              参考知识库总结：
            </h4>
            <div className="text-gray-600 whitespace-pre-wrap">
              {policy}
            </div>
          </div>
          
          {kbCount > 0 && (
            <div className="pt-3 border-t border-gray-200">
              <h4 className="font-semibold text-gray-800 mb-2">
                已参考 {kbCount} 个知识库：
              </h4>
              <ul className="list-disc list-inside space-y-1 text-gray-600">
                {kb_list.map((kb, index) => (
                  <li key={`${kb.name}-${index}`}>{kb.name}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PolicyDisplay;

