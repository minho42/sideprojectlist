import { UserCircleIcon } from "@heroicons/react/solid";

const ProjectItem = ({
  item: { link, fullname, twitter_handle, github_handle, screenshot_url, avatar_url, tags },
  selectedTag,
  setSelectedTag,
}) => {
  const handleTagSelect = (e) => {
    setSelectedTag(e.currentTarget.getAttribute("value"));
  };

  return (
    <div className="flex flex-col items-center justify-start sm:w-1/2 md:w-1/3 lg:w-1/4">
      <div className="border border-gray-400 mx-1 sm:mx-2 my-4 sm:my-3 bg-white rounded-xl shadow-lg">
        <div className="border-b border-gray-400 ">
          <a
            href={link}
            target="_blank"
            rel="noopener noreferrer"
            className="flex flex-col items-center justify-center hover:bg-gray-300 "
          >
            <img className="w-full rounded-t-xl" src={screenshot_url} alt="screenshot" />
          </a>
        </div>

        <div className="px-4 py-2">
          <div className="flex items-center justify-start flex-wrap">
            <div className="flex-shrink-0">
              {avatar_url ? (
                <img className="w-8 rounded-full mr-1" src={avatar_url} alt="twitter avatar" />
              ) : (
                <UserCircleIcon className="w-8 mr-1 text-gray-400" />
              )}
            </div>

            <div className="text-2xl font-semibold">{fullname}</div>
          </div>

          <div className="my-1">
            <div className="flex flex-wrap items-center mt-2 gap-1">
              {tags.map((tag) => {
                return (
                  <div
                    key={tag}
                    value={tag}
                    onClick={handleTagSelect}
                    className={`block cursor-pointer rounded-xl font-medium text-sm px-2 py-1
                      ${
                        selectedTag === tag
                          ? "bg-purple-300 sm:hover:bg-purple-400"
                          : "bg-gray-200 sm:hover:bg-gray-300"
                      }
                      `}
                  >
                    {tag}
                  </div>
                );
              })}
            </div>

            <div className="flex flex-wrap items-center justify-center space-x-4 mt-4 text-sm text-gray-500">
              {twitter_handle ? (
                <div>
                  <a
                    href={`https://twitter.com/${twitter_handle}`}
                    className="hover:underline"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Twitter
                  </a>
                </div>
              ) : (
                ""
              )}
              {github_handle ? (
                <div>
                  <a
                    href={`https://github.com/${github_handle}`}
                    className="hover:underline"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Github
                  </a>
                </div>
              ) : (
                ""
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectItem;
