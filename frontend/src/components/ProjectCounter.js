import { HashtagIcon, XIcon } from "@heroicons/react/outline";

const ProjectCounter = ({ count, selectedTag, setSelectedTag }) => {
  return (
    <div className="flex items-center justify-between">
      {selectedTag ? (
        <div>
          <div className="flex items-center justify-start ">
            <div>
              <HashtagIcon className="w-8 h-8" />
            </div>

            <div>
              {selectedTag} ({count})
            </div>

            <button
              onClick={() => {
                setSelectedTag("");
              }}
              className="text-purple-500 hover:text-purple-600 px-2 py-1"
            >
              <XIcon className="w-8 h-8" />
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div>Projects ({count}) </div>
        </div>
      )}
    </div>
  );
};

export default ProjectCounter;
