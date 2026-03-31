---
layout: post
title: Xcode .gitignore
tags: coding
---

```

# Xcode
.DS_Store
build/
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3
*.xcworkspace
!default.xcworkspace
xcuserdata
profile
*.moved-aside
DerivedData
.idea/
# Pods - for those of you who use CocoaPods
Pods

```

[source](http://stackoverflow.com/questions/18939421/what-should-xcode-6-gitignore-file-include)


```
git rm -r --cached .
git add .
git commit -m "Drop files from .gitignore"
```

[source]https://stackoverflow.com/questions/13541615/how-to-remove-files-that-are-listed-in-the-gitignore-but-still-on-the-repositor)
