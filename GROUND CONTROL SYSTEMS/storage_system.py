from git import Repo
import time

def git_push(REPO_PATH, img_path):
    """
    This function stages, commits, and pushes new images to your GitHub repo.
    
    Parameters:
        img_path (str): path of the image file to commit and push.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        origin.pull()
        repo.index.add(img_path)
        repo.index.commit('Image file uploaded at {}'.format(time.strftime("%H:%M:%S")))
        origin.push()
    except Exception as e:
        return(e)

def main(push = False):  
    REPO_PATH = "/MIT_BWSI_PROJECT"  
    img_path = "Downlink_Data/Images"

    if (push):
        git_push(REPO_PATH=REPO_PATH, img_path=img_path)
        print("Commited & Pushed Images to GitHub Repository")

if __name__ == '__main__':
    main()
