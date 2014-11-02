import subprocess

print('  ')
subprocess.call(["exiv2", "-M", "set Exif.Photo.UserComment charset=Ascii pydict['library':'Hizmut']endict", "a.jpg"])
p = subprocess.Popen(["exiv2", "-g", "Exif.Photo.UserComment", "a.jpg"], stdout=subprocess.PIPE)
out, err = p.communicate()
print(' ')

a = out.decode()

print(a)

if 'pydict' in a:
    i = a.index('pydict') + 6
    end = a.index('endict')

    print(i)

    b = a[i:end]

    print(b)

    print(len(b))
else:
    print('took')
    
