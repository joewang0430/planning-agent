import React from "react";
import { FaDatabase, FaFileAlt } from "react-icons/fa";

interface KnowledgeBaseCardProps {
  name: string;
  type?: "db" | "file";
  selected?: boolean;
  onClick?: () => void;
}

const KnowledgeBaseCard: React.FC<KnowledgeBaseCardProps> = ({ name, type = "db", selected, onClick }) => {
  return (
    <div
      className={`flex flex-row px-4 py-3 rounded-lg shadow-sm border transition cursor-pointer bg-gray-100 hover:bg-blue-100 border-gray-200 ${selected ? "ring-2 ring-blue-400" : ""}`}
      style={{ minHeight: 72, height: 'auto', alignItems: 'center' }}
      onClick={onClick}
    >
      <div style={{width: 32, minWidth: 32, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        {type === "db" ? (
          <FaDatabase style={{fontSize: 24}} className="text-gray-500" />
        ) : (
          <FaFileAlt style={{fontSize: 24}} className="text-gray-400" />
        )}
      </div>
      <div className="flex-1 ml-3">
        <span className="text-sm text-gray-700 whitespace-pre-line break-words" style={{wordBreak: 'break-word'}}>{name}</span>
      </div>
    </div>
  );
};

export default KnowledgeBaseCard;
