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
      className={`flex items-center gap-2 px-4 py-3 rounded-lg shadow-sm border transition cursor-pointer bg-gray-100 hover:bg-blue-100 border-gray-200 ${selected ? "ring-2 ring-blue-400" : ""}`}
      onClick={onClick}
    >
      {type === "db" ? (
        <FaDatabase className="text-2xl text-gray-500" />
      ) : (
        <FaFileAlt className="text-2xl text-gray-400" />
      )}
      <span className="text-base text-gray-700 truncate">{name}</span>
    </div>
  );
};

export default KnowledgeBaseCard;
