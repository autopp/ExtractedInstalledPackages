import sublime, sublime_plugin
import os
import zipfile
import platform
import subprocess

class ExtractInstalledPackageCommand(sublime_plugin.WindowCommand):
  DEFAULT_NAME = "<default>"
  
  def run(self):
    # Get list of Installed Packages
    self.packages_dir_path = sublime.installed_packages_path()
    self.packages_list = [ p for p in os.listdir(self.packages_dir_path) if p.endswith('.sublime-package') ]
    
    # Show quick panel
    self.window.show_quick_panel(self.packages_list, self.on_package_selected)
    
  def on_package_selected(self, index):
    if index < 0:
      return

    package_file_name = self.packages_list[index]
    package_name = os.path.splitext(package_file_name)[0]
    package_file_name = self.packages_dir_path + '/' + package_file_name
    
    # Load plugin setting file
    setting = sublime.load_settings("ExtractInstalledPackages.sublime-settings")
    
    host = platform.node()
    dist_path = setting.get(host, None)
    if dist_path == None:
      # Try to get default case path
      if not setting.has(self.DEFAULT_NAME):
        sublime.error_message("ExtractInstalledPackages: Distination path is not found. (Please check your 'ExtractInstalledPackages.sublime-settings')")
        return
        
      dist_path = settings.get(DEFAULT_NAME)
    
    dist_path = dist_path + '/' + package_name
    
    # Confirm existing file/directory
    if os.path.isfile(dist_path):
      sublime.error_message("ExtractInstalledPackages: '" + dist_path + " is exists and it is file.")
      return
      
    if os.path.isdir(dist_path) and not sublime.ok_cancel_dialog("Do you overwrite '" + dist_path + "'?"):
      return
    
    # Open zip file
    with zipfile.ZipFile(package_file_name) as zf:
      zf.extractall(dist_path)
      
    sublime.status_message("Extract package file")
    
    # Create window and open extraced directory
    subprocess.Popen([sublime.executable_path(), dist_path], cwd=dist_path)
    
  