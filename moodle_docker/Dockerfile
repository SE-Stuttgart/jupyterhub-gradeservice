FROM docker.io/bitnami/moodle:4.1.1

RUN install_packages openssh-client vim git unzip curl watchman

ENV COMPOSER_ALLOW_SUPERUSER=1
RUN composer global config --no-plugins allow-plugins.dealerdirect/phpcodesniffer-composer-installer true
RUN composer global require moodlehq/moodle-cs --no-interaction
ENV PATH="/.composer/vendor/bin:$PATH"

ENV NODE_VERSION 16.20.0
ENV NVM_DIR /usr/local/nvm

RUN mkdir -p $NVM_DIR \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
