"use client";

import { useState } from 'react';
import { ChevronDown, ChevronRight } from 'lucide-react';

interface PolicyDisplayProps {
  policy: string;
}

const PolicyDisplay = ({ policy }: PolicyDisplayProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!policy) {
    return null;
  }

  // Get the first line as a preview when folding
  const firstLine = policy.split('\n')[0];

  return (
    <div className="bg-gray-100 rounded-lg p-3 text-sm text-gray-700 mb-4 transition-all duration-300">
      <div 
        className="flex items-center cursor-pointer select-none"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        {isExpanded ? <ChevronDown size={18} className="mr-1 flex-shrink-0" /> : <ChevronRight size={18} className="mr-1 flex-shrink-0" />}
        <span className="font-medium text-gray-800 mr-2 flex-shrink-0">{isExpanded ? '收起' : '展开'}</span>
        
        {/* When folded, the first row that was correctly truncated is displayed */}
        {!isExpanded && (
          <div className="flex-1 min-w-0">
            <p className="truncate text-gray-600">
              {firstLine}
            </p>
          </div>
        )}
      </div>
      
      {/* When expanded, it displays the complete thought content */}
      {isExpanded && (
        <div className="mt-2 pl-6 text-gray-600 whitespace-pre-wrap animate-fade-in">
          {`思考：\n${policy}`}
        </div>
      )}
    </div>
  );
};

export default PolicyDisplay;

