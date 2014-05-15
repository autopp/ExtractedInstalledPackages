import sublime, sublime_plugin
import os
import zipfile

class ExtractInstalledPackageCommand(sublime_plugin.WindowCommand):
  def run(self):
    # Get list of Installed Packages
    packages_path = sublime.installed_packages_path()
    self.packages_list = [ p for p in os.listdir(packages_path) if p.endswith('.sublime-package') ]
    
    # Show quick panel
    self.show_quick_panel(self.packages_list, on_package_selected)
    
  def on_package_selected(self, index):
    if index < 0:
      return
      
    self.package = self.packages_list[index]
    sublime.message_dialog(self.package)
    return
    # Next, choose distination directory
    
    
  def on_dist_selected(self, text):
    pass
