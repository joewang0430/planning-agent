import React from "react";
import { FaDatabase, FaFileAlt } from "react-icons/fa";

interface KnowledgeBaseCardProps {
  name: string;
  type?: "db" | "file";
  status?: "normal" | "selected" | "added";
  category?: string;
  onClick?: () => void;
}

const KnowledgeBaseCard = ({ name, type = "db", status = "normal", category, onClick }: KnowledgeBaseCardProps) => {
  let cardClass = "flex flex-row px-4 py-3 rounded-lg shadow-sm border cursor-pointer border-gray-200 w-full ";
  let iconClass = "";
  let textClass = "text-sm whitespace-pre-line break-words";

  if (status === "added") {
    cardClass += " bg-gray-200 text-gray-400 cursor-not-allowed opacity-60";
    iconClass = "text-gray-400";
    textClass += " text-gray-400";
  } else if (status === "selected") {
    cardClass += " ring-2 ring-blue-400 bg-blue-100 text-blue-700";
    iconClass = "text-blue-500";
    textClass += " text-blue-700 font-semibold";
  } else {
    cardClass += " bg-gray-100 hover:bg-blue-100 text-gray-700";
    iconClass = type === "db" ? "text-gray-500" : "text-gray-400";
    textClass += " text-gray-700";
  }

  return (
    <div
      className={cardClass}
      style={{ minHeight: 72, alignItems: 'center' }}
      onClick={status === "added" ? undefined : onClick}
    >
      <div style={{width: 32, minWidth: 32, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        {type === "db" ? (
          <FaDatabase style={{fontSize: 24}} className={iconClass} />
        ) : (
          <FaFileAlt style={{fontSize: 24}} className={iconClass} />
        )}
      </div>
      <div className="flex-1 ml-3" style={{ minWidth: 0, width: '1px' }}>
        <span
          className={textClass}
          style={{
            wordBreak: 'break-all',
            overflowWrap: 'anywhere',
            whiteSpace: 'pre-line',
            display: 'block',
            lineHeight: '1.5',
            maxWidth: '100%',
            width: '100%'
          }}
        >
          {name}
        </span>
        {/* 不再显示category，只显示名字 */}
      </div>
    </div>
  );
};

export default KnowledgeBaseCard;
