all:
	python generator.py

clean:
	rm -rf output

install:
	rm -rf /mnt/nas/server/site/mobile /mnt/nas/server/site/desktop
	cp -r output/mobile /mnt/nas/server/site
	cp -r output/desktop /mnt/nas/server/site
	cp output/url.conf /mnt/nas/server/site
	chmod 775 -R /mnt/nas/server/site
	chown server:server -R /mnt/nas/server/site

restart:
	systemctl restart nginx
