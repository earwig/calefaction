module Encryptor
  extend ActiveSupport::Concern

  class_methods do
    def encrypt(value)
      ensure_encryptor
      @crypt.encrypt_and_sign(value)
    end

    def decrypt(value)
      ensure_encryptor
      @crypt.decrypt_and_verify(value)
    end

    private
    def ensure_encryptor
      @crypt ||= ActiveSupport::MessageEncryptor.new(Rails.application.secrets.secret_key_base)
    end
  end
end
